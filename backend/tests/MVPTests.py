from pathlib import Path

import pytest
from django.db import connection
from rest_framework.test import APIClient
from apps.questions.models import AnalyticsEvent, Question
from apps.tags.models import Tag


@pytest.mark.django_db
class TestMVP:
    @pytest.mark.parametrize('query', ['SERIALIZERS', 'simple example', 'python'])
    def test_search_fields(self, api_client, question, query):
        response = api_client.get('/api/questions/list', {'q': query})
        assert response.status_code == 200
        assert [q['id'] for q in response.data] == [question.id]
        event = AnalyticsEvent.objects.get()
        assert event.event_name == 'search'
        assert event.search_query == query
        assert event.user is None

    def test_search_deduplicates_and_does_not_use_list_cache(self, api_client, question):
        question.tag.add(Tag.objects.create(name='Python tips', slug='python-tips'))
        api_client.get('/api/questions/list')
        result = api_client.get('/api/questions/list', {'q': 'python'})
        assert len(result.data) == 1
        assert api_client.get('/api/questions/list', {'q': 'missing'}).data == []
        assert len(api_client.get('/api/questions/list', {'q': '   '}).data) == 1
        assert AnalyticsEvent.objects.count() == 2

    def test_search_saves_user_and_limits_event_text(self, auth_client, user):
        auth_client.get('/api/questions/list', {'q': 'x' * 300})
        event = AnalyticsEvent.objects.get()
        assert event.user == user
        assert len(event.search_query) == 255

    def test_views_and_comments_persist(self, api_client, auth_client, question, user):
        url = f'/api/questions/{question.slug}/retrieve'
        assert APIClient().get(url).status_code == 200
        response = auth_client.post(f'/api/questions/{question.slug}/create_comment', {'text': 'Try this solution.'})
        assert response.status_code == 201
        detail = auth_client.get(url)
        assert detail.data['comments'][0]['text'] == 'Try this solution.'
        assert AnalyticsEvent.objects.filter(event_name='question_view').count() == 2
        assert AnalyticsEvent.objects.filter(user=user, event_name='question_view').count() == 1
        assert api_client.get('/api/questions/missing/retrieve').status_code == 404
        assert AnalyticsEvent.objects.count() == 2

    @pytest.mark.parametrize('description', [None, '', '   '])
    def test_description_required(self, auth_client, description):
        data = {'title': 'A question'}
        if description is not None:
            data['description'] = description
        response = auth_client.post('/api/questions/create', data, format='json')
        assert response.status_code == 400
        assert not AnalyticsEvent.objects.exists()

    def test_create_without_tags_and_event(self, auth_client, user):
        response = auth_client.post('/api/questions/create', {
            'title': 'Как использовать Django?', 'description': 'A short example please.'
        })
        assert response.status_code == 201
        assert response.data['slug']
        event = AnalyticsEvent.objects.get(event_name='question_created')
        assert event.user == user
        assert event.question_id == response.data['id']
        Question.objects.filter(pk=event.question_id).delete()
        event.refresh_from_db()
        assert event.question is None

    def test_sql_queries_use_real_tables(self, auth_client, question):
        auth_client.get('/api/questions/list', {'q': 'python'})
        auth_client.get(f'/api/questions/{question.slug}/retrieve')
        sql = Path(__file__).resolve().parents[2] / 'docs/analytics_queries.sql'
        with connection.cursor() as cursor:
            for query in sql.read_text().split(';'):
                if query.strip():
                    cursor.execute(query)
                    assert cursor.fetchall()

    def test_suggestions_are_limited_and_keep_session(self, api_client, user):
        for i in range(7):
            Question.objects.create(title=f'Django question {i}', description='Example', slug=f'django-{i}', author=user)
        session = '693b8670-ed57-4d63-bde4-168397c0c719'
        result = api_client.get('/api/questions/list', {'q': 'django', 'suggest': '1'}, HTTP_X_SESSION_ID=session)
        assert len(result.data) == 5
        event = AnalyticsEvent.objects.get()
        assert event.session_id == session
        assert event.metadata == {'source': 'suggestion'}
        assert event.user_id is None

    def test_invalid_session_header_is_not_stored(self, api_client, question):
        api_client.get('/api/questions/list', {'q': 'python'}, HTTP_X_SESSION_ID='Bearer not-a-session')
        assert AnalyticsEvent.objects.get().session_id is None

    def test_question_events_share_browser_session(self, auth_client):
        session = '693b8670-ed57-4d63-bde4-168397c0c719'
        created = auth_client.post('/api/questions/create', {'title': 'Session example', 'description': 'Example'}, HTTP_X_SESSION_ID=session)
        assert created.status_code == 201
        auth_client.get(f"/api/questions/{created.data['slug']}/retrieve", HTTP_X_SESSION_ID=session)
        assert AnalyticsEvent.objects.filter(session_id=session).count() == 2

    def test_deleted_question_is_hidden(self, api_client, auth_client, question):
        assert auth_client.delete(f'/api/questions/{question.slug}/destroy').status_code == 204
        assert api_client.get('/api/questions/list').data == []
        assert api_client.get('/api/questions/list', {'q': 'python'}).data == []
        assert api_client.get(f'/api/questions/{question.slug}/retrieve').status_code == 404

    def test_tag_cache_refreshes_after_question_creation(self, api_client, auth_client, tag):
        assert api_client.get(f'/api/tags/{tag.slug}/retrieve').data['questions'] == []
        created = auth_client.post('/api/questions/create', {'title': 'New tagged question', 'description': 'Example', 'tag': [tag.id]})
        assert created.status_code == 201
        assert len(api_client.get(f'/api/tags/{tag.slug}/retrieve').data['questions']) == 1
