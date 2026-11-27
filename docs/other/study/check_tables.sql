-- PostgreSQL: all statements below only read data.
-- Q01 | Database and version
SELECT current_database() AS database_name, current_user AS database_user,
       current_setting('server_version') AS postgres_version;

-- Q02 | Application tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
  AND table_name IN ('users_customuser', 'questions_question', 'tags_tag',
                    'questions_question_tag', 'comments_comments', 'questions_analyticsevent')
ORDER BY table_name;

-- Q03 | Columns, types and nullability
SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('users_customuser', 'questions_question', 'tags_tag',
                    'questions_question_tag', 'comments_comments', 'questions_analyticsevent')
ORDER BY table_name, ordinal_position;

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

-- Q05 | Row counts including soft-deleted rows
SELECT 'users_customuser' AS table_name, COUNT(*) AS rows FROM users_customuser
UNION ALL SELECT 'questions_question', COUNT(*) FROM questions_question
UNION ALL SELECT 'tags_tag', COUNT(*) FROM tags_tag
UNION ALL SELECT 'questions_question_tag', COUNT(*) FROM questions_question_tag
UNION ALL SELECT 'comments_comments', COUNT(*) FROM comments_comments
UNION ALL SELECT 'questions_analyticsevent', COUNT(*) FROM questions_analyticsevent
ORDER BY table_name;

-- Q06 | Demo accounts without password hashes
SELECT id, email, first_name, last_name, is_active
FROM users_customuser WHERE deleted_at IS NULL ORDER BY id;

-- Q07 | Visible questions, authors and tags
SELECT q.id, q.title, u.email AS author,
       COALESCE(string_agg(t.name, ', ' ORDER BY t.name), '(no tags)') AS tags
FROM questions_question q
JOIN users_customuser u ON u.id = q.author_id
LEFT JOIN questions_question_tag qt ON qt.question_id = q.id
LEFT JOIN tags_tag t ON t.id = qt.tag_id
WHERE q.deleted_at IS NULL
GROUP BY q.id, q.title, u.email ORDER BY q.id;

-- Q08 | Comments with their question and author
SELECT c.id, q.title AS question, u.email AS author, c.text
FROM comments_comments c
JOIN questions_question q ON q.id = c.question_id
JOIN users_customuser u ON u.id = c.author_id
WHERE c.deleted_at IS NULL AND q.deleted_at IS NULL ORDER BY c.id;

-- Q09 | Number of comments per visible question, including zero
SELECT q.id, q.title, COUNT(c.id) AS comment_count
FROM questions_question q
LEFT JOIN comments_comments c ON c.question_id = q.id AND c.deleted_at IS NULL
WHERE q.deleted_at IS NULL
GROUP BY q.id, q.title ORDER BY q.id;

-- Q10 | Tag usage on visible questions
SELECT t.name, COUNT(q.id) AS question_count
FROM tags_tag t
LEFT JOIN questions_question_tag qt ON qt.tag_id = t.id
LEFT JOIN questions_question q ON q.id = qt.question_id AND q.deleted_at IS NULL
WHERE t.deleted_at IS NULL
GROUP BY t.id, t.name ORDER BY question_count DESC, t.name;

-- Q11 | Soft delete preserves the database row and its links
SELECT q.id, q.title, q.deleted_at IS NOT NULL AS is_deleted,
       (SELECT COUNT(*) FROM questions_question_tag qt WHERE qt.question_id = q.id) AS tag_links,
       (SELECT COUNT(*) FROM comments_comments c WHERE c.question_id = q.id) AS comments
FROM questions_question q ORDER BY q.id;

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

-- Q13 | Analytics counts: suggestion requests and submitted searches differ
SELECT event_name, COALESCE(metadata->>'source', '-') AS source, COUNT(*) AS events
FROM questions_analyticsevent
GROUP BY event_name, metadata->>'source' ORDER BY event_name, source;

-- Q14 | Recorded search terms and their request sources
SELECT search_query, metadata->>'source' AS source, COUNT(*) AS requests
FROM questions_analyticsevent WHERE event_name = 'search'
GROUP BY search_query, metadata->>'source' ORDER BY search_query, source;

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
