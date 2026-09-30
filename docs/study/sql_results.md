# Фактические результаты проверки

Запуск (UTC): `2026-09-29T20:53:57.542904+00:00`.

Python 3.13.12; Django 5.2.11; PostgreSQL. Данные учебные, не пользовательские.

SQL выполнен через Django cursor в транзакции READ ONLY. Ниже результат каждого из 15 запросов.

## API: проверка CRUD

Запросы выполнены через DRF APIClient внутри Python-процесса с реальной PostgreSQL; браузер и HTTP-сервер не запускались. Для проверки входа использованы настоящие JWT. Временные данные API-проверки откатываются.

| Проверка | HTTP | Ожидалось | Успех |
| --- | --- | --- | --- |
| Registration | 201 | 201 | True |
| JWT login | 200 | 200 | True |
| Anonymous create denied | 401 | 401 | True |
| Empty description rejected | 400 | 400 | True |
| Create question | 201 | 201 | True |
| Read detail | 200 | 200 | True |
| Other author update denied | 403 | 403 | True |
| Other author delete denied | 403 | 403 | True |
| Owner update | 200 | 200 | True |
| Owner updates title | 200 | 200 | True |
| Old slug becomes unavailable | 404 | 404 | True |
| New slug works | 200 | 200 | True |
| Owner soft delete | 204 | 204 | True |
| Deleted detail hidden | 404 | 404 | True |
| Deleted question absent from search | 200 | 200 | True |

## Q01: Database and version

```sql
-- PostgreSQL: all statements below only read data.
-- Q01 | Database and version
SELECT current_database() AS database_name, current_user AS database_user,
       current_setting('server_version') AS postgres_version;
```

| database_name | database_user | postgres_version |
| --- | --- | --- |
| stack_underflow_study | study | 16.15 (Debian 16.15-1.pgdg13+2) |

Строк результата: 1.

## Q02: Application tables

```sql
-- Q02 | Application tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
  AND table_name IN ('users_customuser', 'questions_question', 'tags_tag',
                    'questions_question_tag', 'comments_comments', 'questions_analyticsevent')
ORDER BY table_name;
```

| table_name |
| --- |
| comments_comments |
| questions_analyticsevent |
| questions_question |
| questions_question_tag |
| tags_tag |
| users_customuser |

Строк результата: 6.

## Q03: Columns, types and nullability

```sql
-- Q03 | Columns, types and nullability
SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('users_customuser', 'questions_question', 'tags_tag',
                    'questions_question_tag', 'comments_comments', 'questions_analyticsevent')
ORDER BY table_name, ordinal_position;
```

| table_name | column_name | data_type | is_nullable |
| --- | --- | --- | --- |
| comments_comments | id | bigint | NO |
| comments_comments | created_at | timestamp with time zone | NO |
| comments_comments | updated_at | timestamp with time zone | NO |
| comments_comments | deleted_at | timestamp with time zone | YES |
| comments_comments | text | text | NO |
| comments_comments | author_id | bigint | NO |
| comments_comments | question_id | bigint | NO |
| questions_analyticsevent | id | bigint | NO |
| questions_analyticsevent | event_name | character varying | NO |
| questions_analyticsevent | search_query | character varying | YES |
| questions_analyticsevent | created_at | timestamp with time zone | NO |
| questions_analyticsevent | question_id | bigint | YES |
| questions_analyticsevent | user_id | bigint | YES |
| questions_analyticsevent | metadata | jsonb | YES |
| questions_analyticsevent | session_id | character varying | YES |
| questions_question | id | bigint | NO |
| questions_question | created_at | timestamp with time zone | NO |
| questions_question | updated_at | timestamp with time zone | NO |
| questions_question | deleted_at | timestamp with time zone | YES |
| questions_question | title | character varying | NO |
| questions_question | description | text | YES |
| questions_question | slug | character varying | NO |
| questions_question | is_active | boolean | NO |
| questions_question | author_id | bigint | NO |
| questions_question_tag | id | bigint | NO |
| questions_question_tag | question_id | bigint | NO |
| questions_question_tag | tag_id | bigint | NO |
| tags_tag | id | bigint | NO |
| tags_tag | created_at | timestamp with time zone | NO |
| tags_tag | updated_at | timestamp with time zone | NO |
| tags_tag | deleted_at | timestamp with time zone | YES |
| tags_tag | name | character varying | NO |
| tags_tag | slug | character varying | NO |
| users_customuser | id | bigint | NO |
| users_customuser | last_login | timestamp with time zone | YES |
| users_customuser | is_superuser | boolean | NO |
| users_customuser | created_at | timestamp with time zone | YES |
| users_customuser | updated_at | timestamp with time zone | YES |
| users_customuser | deleted_at | timestamp with time zone | YES |
| users_customuser | email | character varying | NO |
| users_customuser | first_name | character varying | NO |
| users_customuser | last_name | character varying | NO |
| users_customuser | password | character varying | NO |
| users_customuser | is_active | boolean | NO |
| users_customuser | is_staff | boolean | NO |
| users_customuser | avatar | character varying | YES |
| users_customuser | preffered_language | character varying | NO |
| users_customuser | timezone | character varying | NO |

Строк результата: 48.

## Q04: Primary keys, foreign keys and unique constraints

```sql
-- Q04 | Primary keys, foreign keys and unique constraints
SELECT c.conrelid::regclass::text AS table_name, c.contype AS constraint_type,
       pg_get_constraintdef(c.oid) AS definition
FROM pg_constraint c
JOIN pg_class r ON r.oid = c.conrelid
JOIN pg_namespace n ON n.oid = r.relnamespace
WHERE n.nspname = 'public' AND c.contype IN ('p', 'f', 'u')
  AND r.relname IN ('users_customuser', 'questions_question', 'tags_tag',
                   'questions_question_tag', 'comments_comments', 'questions_analyticsevent')
ORDER BY table_name, constraint_type, definition;
```

| table_name | constraint_type | definition |
| --- | --- | --- |
| comments_comments | f | FOREIGN KEY (author_id) REFERENCES users_customuser(id) DEFERRABLE INITIALLY DEFERRED |
| comments_comments | f | FOREIGN KEY (question_id) REFERENCES questions_question(id) DEFERRABLE INITIALLY DEFERRED |
| comments_comments | p | PRIMARY KEY (id) |
| questions_analyticsevent | f | FOREIGN KEY (question_id) REFERENCES questions_question(id) DEFERRABLE INITIALLY DEFERRED |
| questions_analyticsevent | f | FOREIGN KEY (user_id) REFERENCES users_customuser(id) DEFERRABLE INITIALLY DEFERRED |
| questions_analyticsevent | p | PRIMARY KEY (id) |
| questions_question | f | FOREIGN KEY (author_id) REFERENCES users_customuser(id) DEFERRABLE INITIALLY DEFERRED |
| questions_question | p | PRIMARY KEY (id) |
| questions_question | u | UNIQUE (slug) |
| questions_question_tag | f | FOREIGN KEY (question_id) REFERENCES questions_question(id) DEFERRABLE INITIALLY DEFERRED |
| questions_question_tag | f | FOREIGN KEY (tag_id) REFERENCES tags_tag(id) DEFERRABLE INITIALLY DEFERRED |
| questions_question_tag | p | PRIMARY KEY (id) |
| questions_question_tag | u | UNIQUE (question_id, tag_id) |
| tags_tag | p | PRIMARY KEY (id) |
| tags_tag | u | UNIQUE (slug) |
| users_customuser | p | PRIMARY KEY (id) |
| users_customuser | u | UNIQUE (email) |

Строк результата: 17.

## Q05: Row counts including soft-deleted rows

```sql
-- Q05 | Row counts including soft-deleted rows
SELECT 'users_customuser' AS table_name, COUNT(*) AS rows FROM users_customuser
UNION ALL SELECT 'questions_question', COUNT(*) FROM questions_question
UNION ALL SELECT 'tags_tag', COUNT(*) FROM tags_tag
UNION ALL SELECT 'questions_question_tag', COUNT(*) FROM questions_question_tag
UNION ALL SELECT 'comments_comments', COUNT(*) FROM comments_comments
UNION ALL SELECT 'questions_analyticsevent', COUNT(*) FROM questions_analyticsevent
ORDER BY table_name;
```

| table_name | rows |
| --- | --- |
| comments_comments | 3 |
| questions_analyticsevent | 12 |
| questions_question | 4 |
| questions_question_tag | 6 |
| tags_tag | 4 |
| users_customuser | 2 |

Строк результата: 6.

## Q06: Demo accounts without password hashes

```sql
-- Q06 | Demo accounts without password hashes
SELECT id, email, first_name, last_name, is_active
FROM users_customuser WHERE deleted_at IS NULL ORDER BY id;
```

| id | email | first_name | last_name | is_active |
| --- | --- | --- | --- | --- |
| 1 | alice@example.com | Alice | Student | True |
| 2 | bob@example.com | Bob | Student | True |

Строк результата: 2.

## Q07: Visible questions, authors and tags

```sql
-- Q07 | Visible questions, authors and tags
SELECT q.id, q.title, u.email AS author,
       COALESCE(string_agg(t.name, ', ' ORDER BY t.name), '(no tags)') AS tags
FROM questions_question q
JOIN users_customuser u ON u.id = q.author_id
LEFT JOIN questions_question_tag qt ON qt.question_id = q.id
LEFT JOIN tags_tag t ON t.id = qt.tag_id
WHERE q.deleted_at IS NULL
GROUP BY q.id, q.title, u.email ORDER BY q.id;
```

| id | title | author | tags |
| --- | --- | --- | --- |
| 1 | Django serializers explained | alice@example.com | django, python |
| 2 | PostgreSQL unique constraint | alice@example.com | postgresql, python |
| 3 | Angular component communication | alice@example.com | angular |

Строк результата: 3.

## Q08: Comments with their question and author

```sql
-- Q08 | Comments with their question and author
SELECT c.id, q.title AS question, u.email AS author, c.text
FROM comments_comments c
JOIN questions_question q ON q.id = c.question_id
JOIN users_customuser u ON u.id = c.author_id
WHERE c.deleted_at IS NULL AND q.deleted_at IS NULL ORDER BY c.id;
```

| id | question | author | text |
| --- | --- | --- | --- |
| 1 | Django serializers explained | bob@example.com | Use a ModelSerializer. |
| 2 | Django serializers explained | bob@example.com | Call is_valid before save. |
| 3 | PostgreSQL unique constraint | bob@example.com | Add a UNIQUE constraint to the column. |

Строк результата: 3.

## Q09: Number of comments per visible question, including zero

```sql
-- Q09 | Number of comments per visible question, including zero
SELECT q.id, q.title, COUNT(c.id) AS comment_count
FROM questions_question q
LEFT JOIN comments_comments c ON c.question_id = q.id AND c.deleted_at IS NULL
WHERE q.deleted_at IS NULL
GROUP BY q.id, q.title ORDER BY q.id;
```

| id | title | comment_count |
| --- | --- | --- |
| 1 | Django serializers explained | 2 |
| 2 | PostgreSQL unique constraint | 1 |
| 3 | Angular component communication | 0 |

Строк результата: 3.

## Q10: Tag usage on visible questions

```sql
-- Q10 | Tag usage on visible questions
SELECT t.name, COUNT(q.id) AS question_count
FROM tags_tag t
LEFT JOIN questions_question_tag qt ON qt.tag_id = t.id
LEFT JOIN questions_question q ON q.id = qt.question_id AND q.deleted_at IS NULL
WHERE t.deleted_at IS NULL
GROUP BY t.id, t.name ORDER BY question_count DESC, t.name;
```

| name | question_count |
| --- | --- |
| python | 2 |
| angular | 1 |
| django | 1 |
| postgresql | 1 |

Строк результата: 4.

## Q11: Soft delete preserves the database row and its links

```sql
-- Q11 | Soft delete preserves the database row and its links
SELECT q.id, q.title, q.deleted_at IS NOT NULL AS is_deleted,
       (SELECT COUNT(*) FROM questions_question_tag qt WHERE qt.question_id = q.id) AS tag_links,
       (SELECT COUNT(*) FROM comments_comments c WHERE c.question_id = q.id) AS comments
FROM questions_question q ORDER BY q.id;
```

| id | title | is_deleted | tag_links | comments |
| --- | --- | --- | --- | --- |
| 1 | Django serializers explained | False | 2 | 2 |
| 2 | PostgreSQL unique constraint | False | 2 | 1 |
| 3 | Angular component communication | False | 1 | 0 |
| 4 | Python temporary question | True | 1 | 0 |

Строк результата: 4.

## Q12: Current keyword search for python, mirroring icontains

```sql
-- Q12 | Current keyword search for python, mirroring icontains
SELECT DISTINCT q.id, q.title, q.created_at
FROM questions_question q
LEFT JOIN questions_question_tag qt ON qt.question_id = q.id
LEFT JOIN tags_tag t ON t.id = qt.tag_id
WHERE q.deleted_at IS NULL AND (
    UPPER(q.title) LIKE UPPER('%python%')
    OR UPPER(q.description) LIKE UPPER('%python%')
    OR UPPER(t.name) LIKE UPPER('%python%')
)
ORDER BY q.created_at DESC, q.id DESC LIMIT 50;
```

| id | title | created_at |
| --- | --- | --- |
| 2 | PostgreSQL unique constraint | 2026-09-29 20:51:21.849026+00:00 |
| 1 | Django serializers explained | 2026-09-29 20:51:21.831532+00:00 |

Строк результата: 2.

## Q13: Analytics counts: suggestion requests and submitted searches differ

```sql
-- Q13 | Analytics counts: suggestion requests and submitted searches differ
SELECT event_name, COALESCE(metadata->>'source', '-') AS source, COUNT(*) AS events
FROM questions_analyticsevent
GROUP BY event_name, metadata->>'source' ORDER BY event_name, source;
```

| event_name | source | events |
| --- | --- | --- |
| question_created | - | 4 |
| question_view | - | 3 |
| search | submit | 4 |
| search | suggestion | 1 |

Строк результата: 4.

## Q14: Recorded search terms and their request sources

```sql
-- Q14 | Recorded search terms and their request sources
SELECT search_query, metadata->>'source' AS source, COUNT(*) AS requests
FROM questions_analyticsevent WHERE event_name = 'search'
GROUP BY search_query, metadata->>'source' ORDER BY search_query, source;
```

| search_query | source | requests |
| --- | --- | --- |
| avoid duplicate rows | submit | 1 |
| DJANGO | submit | 1 |
| parameterized queries | submit | 1 |
| python | submit | 1 |
| python | suggestion | 1 |

Строк результата: 5.

## Q15: Orphan references and duplicate question/tag pairs (all should be zero)

```sql
-- Q15 | Orphan references and duplicate question/tag pairs (all should be zero)
SELECT 'question_without_author' AS check_name, COUNT(*) AS problems
FROM questions_question q LEFT JOIN users_customuser u ON u.id = q.author_id WHERE u.id IS NULL
UNION ALL
SELECT 'comment_without_question', COUNT(*)
FROM comments_comments c LEFT JOIN questions_question q ON q.id = c.question_id WHERE q.id IS NULL
UNION ALL
SELECT 'comment_without_author', COUNT(*)
FROM comments_comments c LEFT JOIN users_customuser u ON u.id = c.author_id WHERE u.id IS NULL
UNION ALL
SELECT 'tag_link_without_question', COUNT(*)
FROM questions_question_tag qt LEFT JOIN questions_question q ON q.id = qt.question_id WHERE q.id IS NULL
UNION ALL
SELECT 'tag_link_without_tag', COUNT(*)
FROM questions_question_tag qt LEFT JOIN tags_tag t ON t.id = qt.tag_id WHERE t.id IS NULL
UNION ALL
SELECT 'event_without_user', COUNT(*)
FROM questions_analyticsevent e LEFT JOIN users_customuser u ON u.id = e.user_id WHERE e.user_id IS NOT NULL AND u.id IS NULL
UNION ALL
SELECT 'event_without_question', COUNT(*)
FROM questions_analyticsevent e LEFT JOIN questions_question q ON q.id = e.question_id WHERE e.question_id IS NOT NULL AND q.id IS NULL
UNION ALL
SELECT 'duplicate_question_tag_pair', COUNT(*) FROM (
    SELECT question_id, tag_id FROM questions_question_tag
    GROUP BY question_id, tag_id HAVING COUNT(*) > 1
) duplicates ORDER BY check_name;
```

| check_name | problems |
| --- | --- |
| comment_without_author | 0 |
| comment_without_question | 0 |
| duplicate_question_tag_pair | 0 |
| event_without_question | 0 |
| event_without_user | 0 |
| question_without_author | 0 |
| tag_link_without_question | 0 |
| tag_link_without_tag | 0 |

Строк результата: 8.
