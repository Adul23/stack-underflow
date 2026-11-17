# US-08 — Database indexes: EXPLAIN ANALYZE before/after

This doc shows how the US-08 indexes change the question search queries on
PostgreSQL 16 (the `db` service in `docker-compose.yml`) with about 5,000 seeded
questions.

**Headline:** keyword search (`?search=`) went from **12.8 ms to 0.5 ms (~25×)**
for a rare word, and from **11.7 ms to 1.5 ms (~8×)** for `search=django&tag=python`.
PostgreSQL now uses the new trigram indexes instead of reading the whole
`questions_question` table.

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

Measured on 2026-11-17 on a ThinkPad T460s, PostgreSQL 16 (Docker), with 5,000
seeded questions and 14,664 question↔tag links, using
`LOCAL_BACKEND=1 backend/scripts/explain_analyze.sh`. Times are the
"Execution Time" from `EXPLAIN (ANALYZE, BUFFERS)` after three warm-up runs.
Full plans: [before](explain_output/before.md), [after](explain_output/after.md).

| Query (`GET /api/questions/list?...`) | Rows | Before (ms) | After (ms) | Speed-up | Plan change |
|---|---|---|---|---|---|
| `search=deadlock` (rare keyword) | 12 | 12.825 | **0.512** | ~25× | Seq Scan (4,988 rows filtered out) → BitmapOr of `question_title_trgm_idx` + `question_description_trgm_idx` |
| `search=django&tag=python` | 29 | 11.723 | **1.505** | ~8× | Seq Scan → Bitmap Index Scan on `question_title_trgm_idx`, joined with the M2M `tag_id` index |
| `tag=kubernetes` | 476 | 5.983 | 5.945 | none | Unchanged: already used Django's M2M `tag_id` index |
| `q=deadlock` (legacy search box, `LIMIT 50`) | 12 | 36.972 | 35.953 | none | Unchanged: see below |

### Before: `search=deadlock` (key node)

```
Seq Scan on questions_question  (cost=0.00..225.00 rows=1 width=168) (actual time=0.641..12.044 rows=12 loops=1)
  Filter: ((deleted_at IS NULL) AND ((upper((title)::text) ~~ '%DEADLOCK%'::text) OR (upper(description) ~~ '%DEADLOCK%'::text)))
  Rows Removed by Filter: 4988
  Buffers: shared hit=125
...
Execution Time: 12.825 ms
```

### After: `search=deadlock` (key node)

```
Bitmap Heap Scan on questions_question  (cost=112.37..141.30 rows=9 width=168) (actual time=0.058..0.127 rows=12 loops=1)
  Recheck Cond: ((upper((title)::text) ~~ '%DEADLOCK%'::text) OR (upper(description) ~~ '%DEADLOCK%'::text))
  Filter: (deleted_at IS NULL)
  Heap Blocks: exact=12
  ->  BitmapOr  (actual time=0.047..0.048 rows=0 loops=1)
        ->  Bitmap Index Scan on question_title_trgm_idx  (actual time=0.020..0.020 rows=0 loops=1)
              Index Cond: (upper((title)::text) ~~ '%DEADLOCK%'::text)
        ->  Bitmap Index Scan on question_description_trgm_idx  (actual time=0.027..0.027 rows=12 loops=1)
              Index Cond: (upper(description) ~~ '%DEADLOCK%'::text)
...
Execution Time: 0.512 ms
```

### Why two queries did not change

- **`tag=kubernetes`:** the tag filter was already served by Django's built-in
  `questions_question_tag_tag_id` index. Most of the 6 ms goes into joining and
  sorting the 476 matching rows. `tags_tag` has only 30 rows, so PostgreSQL
  correctly reads it directly, and the `UPPER(name)` / `UPPER(slug)` indexes
  only start to matter once there are many tags.
- **Legacy `q=deadlock`:** that query ORs the title/description match with a
  *tag-name* match across a `LEFT JOIN`. Because of that, PostgreSQL has to join
  all 14,664 question↔tag rows first and filter afterwards (`Rows Removed by
  Filter: 14627`), and no index on `questions_question` can help. The new
  `?search=` endpoint does not have this problem. Rewriting the tag part of `q`
  as an `id IN (subquery)` would let it benefit too. That is a possible
  follow-up; it was left out to keep the frontend's current search unchanged.

## Takeaways

- The trigram GIN indexes are what made the difference. They let PostgreSQL
  answer `LIKE '%term%'` searches from an index instead of reading every row.
  This held both for the rare word (12 matches) and for the common one
  (`django`, 332 candidate rows).
- Absolute times are small at 5,000 rows. What matters is the plan change: a
  sequential scan grows linearly with the table, while the index scans grow
  with the number of matches.
- The other indexes (feed ordering, comments, tag `UPPER(...)`) do not affect
  these search queries. They serve other endpoints, or only start to matter at
  larger data sizes.
