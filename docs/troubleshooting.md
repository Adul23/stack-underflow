# Troubleshooting

| Problem | Checks and suggested action |
|---|---|
| Database connection refused | Run `docker compose --env-file backend/.env ps`; check port 5432, database credentials and DB_HOST. Use `127.0.0.1` for local Django and `db` inside Compose. |
| Missing secret or settings error | Compare private `backend/.env` with `.env.example`; generate a secret and do not commit it. |
| Port 8000 already used | Stop the duplicate backend or use only one installation option. |
| Missing database tables | Activate the environment and run `python manage.py migrate` from backend, or use the Compose equivalent. |
| Angular cannot reach API | Check the backend is running, the configured API URL and browser network errors. |
| CORS error | Match the exact frontend origin in `CORS_ALLOWED_ORIGINS`; do not allow all origins as a production workaround. |
| Empty question list | Create a question or run `python seed_demo.py` from backend. |
| Analytics 401 or 403 | Sign in with a staff account; do not remove API permission checks. |
| Browser tests fail to launch | Install Chrome and check ChromeHeadless configuration. |
| Test database permission error | The PostgreSQL test user needs CREATEDB. Use a disposable development database. |
| Build cannot fetch fonts | Check internet access; the production build uses Google Fonts. |

## Diagnostics

```bash
docker compose --env-file backend/.env ps
docker compose --env-file backend/.env logs --tail=100 backend
```

For local Django run `python manage.py check` from `backend/`. For frontend run `npm run build` from `frontend/`. Do not share logs containing secrets or personal data. Report reproducible non-sensitive bugs using [CONTRIBUTING](../CONTRIBUTING.md); follow [SECURITY](../SECURITY.md) for vulnerabilities. These are suggested checks, not a record of reproduced failures.
