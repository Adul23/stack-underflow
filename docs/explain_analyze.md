# US-08 — Database indexes: EXPLAIN ANALYZE before/after

This doc shows how the US-08 indexes change the question search queries on
PostgreSQL 16 (the `db` service in `docker-compose.yml`) with about 5,000 seeded
questions.

> **Status: timings not yet recorded.** The indexes, seed command and measurement
> script are done and tested. The numbers below must come from a real run of
> `backend/scripts/explain_analyze.sh`. Do not fill them in by hand.

## Indexes added

| Index | Table / columns | Serves | Migration |
|---|---|---|---|
| `question_live_created_idx` | `questions_question (created_at DESC, id DESC) WHERE deleted_at IS NULL` (partial) | Feed and search ordering: `WHERE deleted_at IS NULL ORDER BY created_at DESC, id DESC [LIMIT 50]` | `questions/0005_search_indexes` |
| `question_active_created_idx` | `questions_question (is_active, created_at DESC)` | Filtering active questions newest-first | `questions/0005_search_indexes` |
| `question_title_trgm_idx` | `questions_question USING gin (UPPER(title::text) gin_trgm_ops)`, PostgreSQL only | `?search=` / `?q=`: Django's `icontains` becomes `UPPER(title::text) LIKE UPPER('%term%')`, which a B-tree cannot use | `questions/0005_search_indexes` |
| `question_description_trgm_idx` | same on `description` | same | `questions/0005_search_indexes` |
| `comment_question_created_idx` | `comments_comments (question_id, created_at)` | Comments of a question, in order (question detail page) | `comments/0003_comment_question_created_idx` |
| `tag_name_upper_idx`, `tag_slug_upper_idx` | `tags_tag (UPPER(name))`, `tags_tag (UPPER(slug))` | `?tag=` uses a case-insensitive `UPPER(...) = UPPER(...)` match | `tags/0002_tag_lookup_indexes` |

**Already covered, so not added again:**

- `questions_question.slug` is `unique=True`, which already creates a B-tree index.
  That index serves `/questions/<slug>/retrieve`.
- The question↔tag M2M table (`questions_question_tag`) already has Django's
  indexes on `question_id` and on `tag_id`, plus a unique `(question_id, tag_id)`
  index. Both join directions are covered.

**Notes:**

- The trigram indexes need the `pg_trgm` extension. The migration runs
  `CREATE EXTENSION IF NOT EXISTS pg_trgm`. On PG13+ pg_trgm is a trusted
  extension, so the database owner can create it without superuser rights. On
  SQLite (local tests) this step is skipped.
- `is_active` is not filtered on by any endpoint yet. That index only pays off
  once a query filters on it.

## How to reproduce

From the repository root, with Docker running and `backend/.env` configured:

```bash
backend/scripts/explain_analyze.sh
```

The script:

1. Starts `db` and `backend` and applies all migrations.
2. Runs `python manage.py seed_bulk --flush --count 5000`. The seed is
   deterministic: 5,000 questions, 30 tags, 2–4 tags per question, and a rare
   keyword in about 1% of questions.
3. **Before:** runs `migrate tags 0001`, which rolls back the three US-08 index
   migrations, then `ANALYZE`, then `python manage.py explain_search`, writing
   `docs/explain_output/before.md`.
4. **After:** runs `migrate`, which re-applies them, then `ANALYZE`, then
   `explain_search`, writing `docs/explain_output/after.md`.

`explain_search` builds the queries with the same code the API uses
(`QuestionViewSet.search_queryset`). It warms each query up three times, then
prints `EXPLAIN (ANALYZE, BUFFERS)` for it.

## Results

PostgreSQL 16 (Docker), 5,000 questions. Times are "Execution Time" from
`EXPLAIN ANALYZE`, in milliseconds.

| Query (`GET /api/questions/list?...`) | Rows | Before (ms) | After (ms) | Plan change |
|---|---|---|---|---|
| `search=deadlock` (rare keyword) | _pending_ | _pending_ | _pending_ | _pending_ |
| `search=django&tag=python` | _pending_ | _pending_ | _pending_ | _pending_ |
| `tag=kubernetes` | _pending_ | _pending_ | _pending_ | _pending_ |
| `q=deadlock` (legacy search box, `LIMIT 50`) | _pending_ | _pending_ | _pending_ | _pending_ |

### Before: `search=deadlock`

```
pending: paste from docs/explain_output/before.md
```

### After: `search=deadlock`

```
pending: paste from docs/explain_output/after.md
```

## What to expect when reading the results

- **Rare keyword:** this is where the trigram GIN index matters. Before, the plan
  should show a `Seq Scan` on `questions_question` with a `Filter: upper(title)
  ~~ '%DEADLOCK%'`. After, it should show a `Bitmap Index Scan` on
  `question_title_trgm_idx` / `question_description_trgm_idx`.
- **Common keyword (`django`):** this term appears in a large share of rows, so
  PostgreSQL may still choose a sequential scan after the indexes exist. That is
  correct planner behaviour, not a missing index. The difference grows with
  table size.
- **5,000 rows is small.** Absolute times will be a few milliseconds either way.
  The plan change (seq scan → index scan) is the main result, and it is what
  keeps the query fast as the table grows.
