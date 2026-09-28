-- These table names match the Django models. Works with SQLite and PostgreSQL.

-- Questions created per day
SELECT DATE(created_at) AS day, COUNT(*) AS questions_created
FROM questions_question
GROUP BY DATE(created_at)
ORDER BY day;

-- Searches per day
SELECT DATE(created_at) AS day, COUNT(*) AS searches
FROM questions_analyticsevent
WHERE event_name = 'search'
GROUP BY DATE(created_at)
ORDER BY day;

-- Popular searches
SELECT search_query, COUNT(*) AS searches
FROM questions_analyticsevent
WHERE event_name = 'search'
GROUP BY search_query
ORDER BY searches DESC;

-- Most viewed questions
SELECT q.id, q.title, COUNT(*) AS views
FROM questions_analyticsevent e
JOIN questions_question q ON q.id = e.question_id
WHERE e.event_name = 'question_view'
GROUP BY q.id, q.title
ORDER BY views DESC;

-- Recent events for the demo
SELECT id, event_name, user_id, question_id, search_query, created_at
FROM questions_analyticsevent
ORDER BY created_at DESC
LIMIT 20;
