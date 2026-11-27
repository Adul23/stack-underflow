# API guide

Local base URL: `http://127.0.0.1:8000/api`. Use the live [Swagger UI](http://127.0.0.1:8000/api/docs/) or [OpenAPI schema](http://127.0.0.1:8000/api/schema/) for request fields and response schemas. The table covers the main MVP actions, not every legacy route. Paths below are relative to `/api`.

| Method | Path | Access |
|---|---|---|
| POST | `/users/register` | Public |
| POST | `/users/login` | Public |
| POST | `/users/token/refresh` | Refresh token |
| GET | `/questions/list` | Public |
| GET | `/questions/{slug}/retrieve` | Public |
| POST | `/questions/create` | Authenticated |
| PATCH | `/questions/{slug}/update` | Authenticated owner |
| DELETE | `/questions/{slug}/destroy` | Authenticated owner |
| POST | `/questions/{slug}/create_comment` | Authenticated |
| GET | `/tags/list` | Public |
| GET | `/tags/{slug}/retrieve` | Public |
| GET | `/analytics/summary/` | Staff only |

## Examples

```bash
curl 'http://127.0.0.1:8000/api/questions/list?search=django&tag=python'
curl 'http://127.0.0.1:8000/api/tags/list'
curl -H 'Authorization: Bearer <access-token>' 'http://127.0.0.1:8000/api/analytics/summary/'
```

Replace placeholders locally. Never publish real tokens. Use Swagger to inspect required request bodies before sending writes. The analytics response contains `totals` with `question_view`, `question_create` and `search`, plus `top_questions` with question ID, title, slug and views. Anonymous analytics requests return 401 and ordinary authenticated users return 403 according to the existing analytics documentation.

## Search and tracking

The list accepts `search` (or `q`) and `tag`. A valid optional `X-Session-ID` UUID links events in a browser tab; it is not an authentication credential. Search text can be stored, so never send secrets as queries. See [analytics](analytics.md) and [privacy](../PRIVACY.md).

The router paths were checked against the Django source. The checked-in `backend/schema.yml` may lag behind the current routes; prefer the live schema. Requests were not executed for this documentation update.
