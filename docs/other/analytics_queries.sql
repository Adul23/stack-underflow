-- A. Questions created per day, including questions later soft-deleted.
SELECT DATE(created_at) AS day, COUNT(*) AS questions_created
FROM questions_question
GROUP BY DATE(created_at)
ORDER BY day;

-- B. Search requests per day (debounced suggestions and submitted searches).
SELECT DATE(created_at) AS day, COUNT(*) AS searches
FROM questions_analyticsevent
WHERE event_name = 'search'
GROUP BY DATE(created_at)
ORDER BY day;

-- C. Most common queries, ignoring letter case and surrounding spaces.
SELECT LOWER(TRIM(search_query)) AS query, COUNT(*) AS searches
FROM questions_analyticsevent
WHERE event_name = 'search'
GROUP BY LOWER(TRIM(search_query))
ORDER BY searches DESC;

-- D. Most viewed questions. A successful detail request counts as a view.
SELECT q.id, q.title, COUNT(*) AS views
FROM questions_analyticsevent e
JOIN questions_question q ON q.id = e.question_id
WHERE e.event_name = 'question_view'
GROUP BY q.id, q.title
ORDER BY views DESC;

-- E. Most frequently used tags on non-deleted questions.
SELECT t.id, t.name, COUNT(*) AS questions
FROM tags_tag t
JOIN questions_question_tag qt ON qt.tag_id = t.id
JOIN questions_question q ON q.id = qt.question_id
WHERE q.deleted_at IS NULL
GROUP BY t.id, t.name
ORDER BY questions DESC;

-- F. Distinct users and browser sessions with recorded actions per day.
-- These are separate counts: one user can have several browser sessions.
SELECT DATE(created_at) AS day,
       COUNT(DISTINCT user_id) AS active_users,
       COUNT(DISTINCT session_id) AS active_sessions
FROM questions_analyticsevent
GROUP BY DATE(created_at)
ORDER BY day;

-- Recent event records for the teacher demo.
SELECT id, event_name, user_id, question_id, session_id, search_query, metadata, created_at
FROM questions_analyticsevent
ORDER BY created_at DESC
LIMIT 20;
