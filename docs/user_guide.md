# User guide

Stack Underflow is a Q&A platform for sharing technical and educational knowledge.

| Page | Purpose |
|---|---|
| `/home` | Entry page |
| `/questions` | Browse and search questions |
| `/questions/:slug` | Read a question and its comments |
| `/tags`, `/tags/:slug` | Browse topics |
| `/signup`, `/login` | Create an account and sign in |
| `/newquestion` | Ask a question after signing in |
| `/questions/edit/:slug` | Edit your own question |
| `/analytics` | Staff analytics; API access is restricted |

## Ask and answer

1. Open Sign up and create an account. Sign in.
2. Select Ask Question. Enter a clear title and description, and add relevant tags such as `python` and `django`.
3. Submit the question and open its detail page.
4. To answer a question, open its detail page and submit a comment while signed in.
5. Use the edit or delete controls for your own questions where available.

## Find information

Open Questions, type a keyword such as `paginate`, and wait for suggestions (300 ms debounce, up to five results). Press Search for the full results. Select a tag to narrow results, or click a tag chip. Clear the filters to return to the list. Search is keyword-based, not AI or semantic search.

## Staff analytics

Sign in with a staff account and open `/analytics`. The dashboard shows lifetime totals for searches, views and question creation, and up to five most viewed active questions. These are event counts, not unique visitors. See [analytics](analytics.md).

## Safe participation

Do not publish passwords, private information or abusive content in questions, comments or search. Follow the [Code of Conduct](../CODE_OF_CONDUCT.md) and [Privacy Policy](../PRIVACY.md). For problems, contact maintainers without posting sensitive details publicly. A dedicated private reporting channel is not yet confirmed.
