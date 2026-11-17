# Analytics

An event is one stored action. Events live in `questions_analyticsevent` in the
same PostgreSQL database as questions. Django admin shows them under Questions.

| Event | Created when |
| --- | --- |
| `search` | A nonempty `q` or `search` is sent to the question list endpoint, including a debounced suggestion request. A `tag` filter alone is not recorded. |
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
| `metadata` | Nullable JSONB. Search records contain source (suggestion or submit) and, for `search` with a tag filter, the tag value. |
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


## Dashboard (US-10)

Open `/analytics` in the Angular app after signing in as a staff user
(`is_staff=True`). The backend enforces staff access: anonymous requests return
401, ordinary users return 403. `GET /api/analytics/summary/` returns lifetime
`totals` (question_view, question_create, search) and `top_questions` (up to five,
ordered by views descending, ties by question ID). Deleted questions are excluded
from the ranking; historical events still count in totals.

The existing AnalyticsEvent table is retained to preserve data and compatibility.
The analytics app provides aggregation; `question_created` is exposed as
`question_create` in the API. The event_name + created_at index is migration 0006.

### Fill the database for a presentation

From `backend`, using your configured environment:

```sh
python manage.py migrate
python manage.py seed_bulk --count 5000
python manage.py seed_analytics --count 500
python manage.py createsuperuser
```

`seed_bulk` creates questions and tags; `seed_analytics` adds explicitly synthetic
activity across the last seven days. It never assigns synthetic actions to real
users. Rerunning replaces only its own marked events. Do not use synthetic counts
as evidence of real usage. No public event-write endpoint is exposed.

For Docker, prefix each command with
`docker compose --env-file backend/.env exec backend` from the repository root.

### Demo

1. Log in as an administrator and open Analytics; show the three counters and ranking.
2. Open a question, search for django, then create a question with tags.
3. Return to Analytics and click Refresh: the relevant totals increase.
4. Show that an ordinary user cannot access the analytics API.

Counts are request-based, not unique users. Tag-only filtering currently does not
record a keyword search event; keyword and legacy q searches do.
