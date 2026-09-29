# Analytics

An event is one stored action. Events live in `questions_analyticsevent` in the
same PostgreSQL database as questions. Django admin shows them under Questions.

| Event | Created when |
| --- | --- |
| `search` | A nonempty `q` is sent to the question list endpoint, including a debounced suggestion request. |
| `question_view` | A question detail request succeeds, including opening a suggestion. Reloading counts again. |
| `question_created` | An authenticated user successfully creates a question and its tag links. |

| Field | Meaning |
| --- | --- |
| `id` | Generated bigint primary key. |
| `event_name` | Action name, up to 100 characters. |
| `user_id` | Nullable foreign key to users_customuser; NULL for anonymous visitors. |
| `question_id` | Nullable foreign key to questions_question. |
| `session_id` | Nullable browser session UUID (varchar 64). |
| `search_query` | Nullable search text, trimmed and limited to 255 characters in the event. |
| `metadata` | Nullable JSONB. Search records contain only source: suggestion or submit. |
| `created_at` | Automatic timestamp with time zone. |

The Angular interceptor generates a random UUID in sessionStorage and sends it
as `X-Session-ID` only to the configured API. It survives reloads in that tab.
Django accepts only valid UUIDs and writes events directly in the question views.
No separate analytics service or public event-write endpoint is needed. API
clients without this header still work; their session field is NULL.

We do not copy passwords, JWTs, email addresses, request bodies or arbitrary
headers into analytics. Search text is stored, so users should not enter secrets
in search. Metadata is set by the backend, not copied from the request.

Empty searches and failed detail/creation requests do not create events. A
suggestion request waits 300 ms after typing stops. Counts therefore measure
search requests, not individual keypresses or unique people. The SQL counts
users and sessions separately; it does not add them together. Normal page loads
and comments are not tracked in this MVP.

Run the analyses from the repository root:

```bash
docker compose --env-file backend/.env exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1' < docs/analytics_queries.sql
```

For a managed PostgreSQL database, run `psql` with its connection environment
(PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD, PGSSLMODE):

```bash
psql -v ON_ERROR_STOP=1 -f docs/analytics_queries.sql
```
