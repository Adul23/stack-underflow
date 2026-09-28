# STACK UNDERFLOW — TSIS 3

## MVP Scope

We kept only the basic functionality in the demo: login, registration, questions,
comments, tags, search and analytics. We reused the existing Angular pages and
Django apps. Other old code is still in the project.

## Database

We use CustomUser, Question, Tag and Comments. Questions have an author and many
tags. Comments belong to a question and a user. The only new model is
AnalyticsEvent. See [the database diagram](database_schema.md).

## Question Interface

Users can see questions, create questions, open questions, use tags and leave
comments. Creating a question needs a title and description. Tags are optional.
Login is needed to create questions and comments.

## Analytics

User actions are saved directly in AnalyticsEvent: `search`, `question_view` and
`question_created`. Anonymous searches and views have no user. Every successful
question detail request records a view. Empty searches show all questions and do
not save an event. Search text in analytics is limited to 255 characters.
We can show records in Django admin and run [these SQL queries](analytics_queries.sql).

## Search

We implemented simple search by question title, description and tags. For MVP we
did not use embeddings or vector databases. The Search button calls
`GET /api/questions/list?q=python`. Matching ignores case and removes duplicates.
This is keyword search, not AI semantic search.

## Branding

The application is named STACK UNDERFLOW. Technical names use stack-underflow
or stack_underflow.

## Run locally

Follow the commands in [README](../README.md). Local Django uses SQLite and Docker
uses PostgreSQL. The frontend is in `frontend/`, the backend is in `backend/`,
and the Django configuration package is `stack_underflow`.

## Teacher demo

1. Open the site, register with an email and a password of at least 8 characters,
   then log in. Use a password that is not common or entirely numeric.
2. Ask a question with a description and tags such as `python` and `django`.
3. Open Questions and search for part of its title, then for `python`.
4. Open the question, add a comment, and reload to show it was saved.
5. Log into Django admin with the superuser to show users, questions, tags,
   comments and Analytics events (under Questions).
6. Run the SQL queries. With SQLite, from the repository root:

```bash
sqlite3 backend/db.sqlite3 < docs/analytics_queries.sql
```

If the sqlite3 command is unavailable, use Python instead:

```bash
python3 - <<'PY'
import sqlite3
from pathlib import Path
with sqlite3.connect('backend/db.sqlite3') as db:
    print(db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    for query in Path('docs/analytics_queries.sql').read_text().split(';'):
        if query.strip():
            print(db.execute(query).fetchall())
PY
```

For PostgreSQL, run from the repository root:

```bash
docker compose --env-file backend/.env exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < docs/analytics_queries.sql
```
