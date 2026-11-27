"""Run the real Django API/SQL against a separate, persistent PostgreSQL demo DB."""
import argparse
import io
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
sys.stdout.reconfigure(encoding='utf-8')


def configure():
    from decouple import RepositoryEnv
    values = RepositoryEnv(str(ROOT / '.env.study'))
    for key in ('STACK_UNDERFLOW_ENV_ID', 'STACK_UNDERFLOW_SECRET_KEY', 'DB_NAME',
                'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'USE_REDIS'):
        os.environ[key] = values[key]
    if os.environ['DB_NAME'] != 'stack_underflow_study' or os.environ['DB_HOST'] != '127.0.0.1':
        raise RuntimeError('This demo requires the isolated local stack_underflow_study database.')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'stack_underflow.env.local'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import django
    django.setup()


def require(response, code):
    if response.status_code != code:
        raise AssertionError(f'Expected HTTP {code}, received {response.status_code}: {response.data}')
    return response.data


def seed():
    from django.db import transaction
    from apps.users.models import CustomUser
    from apps.tags.models import Tag
    from apps.questions.models import Question, AnalyticsEvent
    from apps.comments.models import Comments
    from rest_framework.test import APIClient

    expected_titles = ['Django serializers explained', 'PostgreSQL unique constraint',
                       'Angular component communication', 'Python temporary question']
    if Question.objects.filter(title__in=expected_titles).count() == 4:
        print('Existing study dataset retained.')
        return
    if any(model.objects.exists() for model in (CustomUser, Tag, Question, AnalyticsEvent, Comments)):
        raise RuntimeError('The study DB contains unfamiliar data. No existing rows were changed.')
    with transaction.atomic():
        alice = CustomUser.objects.create_user('alice@example.com', 'Alice', 'Student', None)
        bob = CustomUser.objects.create_user('bob@example.com', 'Bob', 'Student', None)
        tags = {name: Tag.objects.create(name=name, slug=name) for name in ('python', 'django', 'postgresql', 'angular')}
        author = APIClient()
        author.force_authenticate(user=alice)
        author.credentials(HTTP_X_SESSION_ID='11111111-1111-4111-8111-111111111111')
        records = [
            (expected_titles[0], 'Validate request data and convert model objects to JSON.', ['python', 'django']),
            (expected_titles[1], 'Use parameterized queries and a UNIQUE constraint.', ['python', 'postgresql']),
            (expected_titles[2], 'Pass data with Input and Output.', ['angular']),
            (expected_titles[3], 'This row demonstrates soft deletion.', ['python']),
        ]
        questions = []
        for title, description, names in records:
            data = require(author.post('/api/questions/create', {
                'title': title, 'description': description, 'tag': [tags[name].id for name in names]
            }, format='json'), 201)
            questions.append(data)
        commenter = APIClient()
        commenter.force_authenticate(user=bob)
        for index, text in [(0, 'Use a ModelSerializer.'), (0, 'Call is_valid before save.'),
                            (1, 'Add a UNIQUE constraint to the column.')]:
            require(commenter.post(f"/api/questions/{questions[index]['slug']}/create_comment", {'text': text}), 201)
        require(author.delete(f"/api/questions/{questions[3]['slug']}/destroy"), 204)
        visitor = APIClient()
        visitor.credentials(HTTP_X_SESSION_ID='22222222-2222-4222-8222-222222222222')
        examples = []
        for query, suggest, expected in [('python', False, 2), ('DJANGO', False, 1),
                                         ('parameterized queries', False, 1),
                                         ('avoid duplicate rows', False, 0), ('python', True, 2)]:
            data = require(visitor.get('/api/questions/list', {'q': query, 'suggest': '1' if suggest else '0'}), 200)
            assert len(data) == expected, (query, data)
            examples.append({'query': query, 'suggest': suggest, 'count': len(data),
                             'titles': [item['title'] for item in data]})
        for index in (0, 0, 1):
            require(visitor.get(f"/api/questions/{questions[index]['slug']}/retrieve"), 200)
    (HERE / 'search_examples.json').write_text(json.dumps(examples, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Study dataset created through the real question/comment API; accounts and tags created via ORM.')


def verify_api():
    from django.db import transaction
    from rest_framework.test import APIClient
    from rest_framework_simplejwt.tokens import RefreshToken
    from apps.users.models import CustomUser
    from apps.questions.models import Question
    checks = []

    def record(label, response, expected):
        data = require(response, expected)
        checks.append({'check': label, 'status': response.status_code, 'expected': expected, 'passed': True})
        return data

    # Only these temporary probe records are rolled back; the demonstration dataset stays.
    with transaction.atomic():
        guest = APIClient()
        email = f'probe-{secrets.token_hex(5)}@example.com'
        password = secrets.token_urlsafe(24)
        record('Registration', guest.post('/api/users/register', {'email': email, 'password': password,
               'first_name': 'Probe', 'last_name': 'Student'}, format='json'), 201)
        login = record('JWT login', guest.post('/api/users/login', {'email': email, 'password': password}), 200)
        owner = APIClient()
        owner.credentials(HTTP_AUTHORIZATION=f"Bearer {login['access']}")
        record('Anonymous create denied', guest.post('/api/questions/create', {'title': 'Probe', 'description': 'Example'}), 401)
        record('Empty description rejected', owner.post('/api/questions/create', {'title': 'Probe', 'description': ''}), 400)
        created = record('Create question', owner.post('/api/questions/create', {
            'title': 'CRUD probe', 'description': 'A temporary question for CRUD verification.'}), 201)
        slug = created['slug']
        record('Read detail', guest.get(f'/api/questions/{slug}/retrieve'), 200)
        other = APIClient()
        other.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(CustomUser.objects.get(email='bob@example.com')).access_token}")
        record('Other author update denied', other.patch(f'/api/questions/{slug}/update', {'description': 'Forbidden'}), 403)
        record('Other author delete denied', other.delete(f'/api/questions/{slug}/destroy'), 403)
        record('Owner update', owner.patch(f'/api/questions/{slug}/update', {'description': 'Updated content'}), 200)
        question = Question.objects.get(pk=created['id'])
        assert question.description == 'Updated content'
        record('Owner updates title', owner.patch(f'/api/questions/{slug}/update', {'title': 'Renamed CRUD probe'}), 200)
        question.refresh_from_db()
        assert question.slug != slug
        record('Old slug becomes unavailable', guest.get(f'/api/questions/{slug}/retrieve'), 404)
        slug = question.slug
        record('New slug works', guest.get(f'/api/questions/{slug}/retrieve'), 200)
        record('Owner soft delete', owner.delete(f'/api/questions/{slug}/destroy'), 204)
        question.refresh_from_db()
        assert question.deleted_at is not None
        record('Deleted detail hidden', guest.get(f'/api/questions/{slug}/retrieve'), 404)
        result = record('Deleted question absent from search', guest.get('/api/questions/list', {'q': 'Renamed CRUD probe'}), 200)
        assert result == []
        transaction.set_rollback(True)
    return checks


def execute_queries():
    from django.db import connection, transaction
    import sqlparse
    results = []
    # PostgreSQL enforces read-only execution for every supplied SQL example.
    with transaction.atomic(), connection.cursor() as cursor:
        cursor.execute('SET TRANSACTION READ ONLY')
        for statement in sqlparse.split((HERE / 'check_tables.sql').read_text(encoding='utf-8')):
            match = re.search(r'-- (Q\d+) \| (.+)', statement)
            if not match:
                continue
            cursor.execute(statement)
            results.append({'id': match[1], 'title': match[2], 'sql': statement,
                            'columns': [col[0] for col in cursor.description], 'rows': cursor.fetchall()})
    assert len(results) == 15
    integrity = next(result for result in results if result['id'] == 'Q15')
    assert all(row[1] == 0 for row in integrity['rows'])
    return results


def md_table(columns, rows):
    def cell(value):
        return str(value if value is not None else 'NULL').replace('|', '\\|').replace('\n', '<br>')
    return '\n'.join(['| ' + ' | '.join(columns) + ' |', '| ' + ' | '.join(['---'] * len(columns)) + ' |'] +
                     ['| ' + ' | '.join(map(cell, row)) + ' |' for row in rows])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tests', action='store_true')
    args = parser.parse_args()
    configure()
    from django.core.management import call_command
    from django.db import connection
    import django

    check_log = io.StringIO()
    call_command('check', stdout=check_log)
    call_command('migrate', interactive=False, stdout=check_log)
    call_command('makemigrations', check=True, dry_run=True, stdout=check_log)
    (HERE / 'django_checks.txt').write_text(check_log.getvalue(), encoding='utf-8')
    seed()
    api = verify_api()
    results = execute_queries()
    run = {'executed_at_utc': datetime.now(timezone.utc).isoformat(), 'python': sys.version.split()[0],
           'django': django.get_version(), 'database_vendor': connection.vendor,
           'api_transport': 'Django REST Framework APIClient (in process, real PostgreSQL)',
           'api_checks': api, 'queries': results}
    (HERE / 'verification.json').write_text(json.dumps(run, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    lines = ['# Фактические результаты проверки', '', f"Запуск (UTC): `{run['executed_at_utc']}`.", '',
             f"Python {run['python']}; Django {run['django']}; PostgreSQL. Данные учебные, не пользовательские.", '',
             'SQL выполнен через Django cursor в транзакции READ ONLY. Ниже результат каждого из 15 запросов.', '',
             '## API: проверка CRUD', '',
             'Запросы выполнены через DRF APIClient внутри Python-процесса с реальной PostgreSQL; браузер и HTTP-сервер не запускались. '
             'Для проверки входа использованы настоящие JWT. Временные данные API-проверки откатываются.', '',
             md_table(['Проверка', 'HTTP', 'Ожидалось', 'Успех'], [[v['check'], v['status'], v['expected'], v['passed']] for v in api]), '']
    for result in results:
        lines.extend([f"## {result['id']}: {result['title']}", '', '```sql', result['sql'], '```', '',
                      md_table(result['columns'], result['rows']), '', f"Строк результата: {len(result['rows'])}.", ''])
    (HERE / 'sql_results.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f"PASS: {len(api)} API checks, {len(results)} SQL queries, all integrity checks = 0.")
    if args.tests:
        command = [sys.executable, '-m', 'pytest', 'tests/MVPTests.py', 'tests/QuestionsTests.py',
                   'tests/UsersTests.py', 'tests/TagsTests.py', 'tests/CommentsTests.py', '-q']
        completed = subprocess.run(command, cwd=ROOT / 'backend', capture_output=True, text=True, encoding='utf-8')
        (HERE / 'backend_tests.txt').write_text(completed.stdout + completed.stderr, encoding='utf-8')
        print(completed.stdout)
        if completed.returncode:
            print(completed.stderr)
            raise SystemExit(completed.returncode)


if __name__ == '__main__':
    main()
