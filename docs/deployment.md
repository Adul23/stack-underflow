# Deploy the MVP

Architecture: static Angular frontend → Django REST API → PostgreSQL.
Redis, Celery and WebSockets are not required for this flow. The old optional
Docker services can be started with `--profile legacy` if needed separately.

No public deployment was performed: this workspace has no configured hosting
provider credentials. The remaining external step is to create/connect a hosting
project with a static site, Python web service and managed PostgreSQL database,
then apply the settings and commands below. No provider-specific framework is needed.

## Backend environment

Set these in the web service's private environment; never commit them:

```dotenv
STACK_UNDERFLOW_ENV_ID=prod
STACK_UNDERFLOW_SECRET_KEY=<random secret generated locally>
ALLOWED_HOSTS=api.your-domain.example
CORS_ALLOWED_ORIGINS=https://your-frontend.example
CSRF_TRUSTED_ORIGINS=https://api.your-domain.example
DB_NAME=<database name>
DB_USER=<database user>
DB_PASSWORD=<database password>
DB_HOST=<database host>
DB_PORT=5432
DB_SSLMODE=require
SECURE_SSL_REDIRECT=True
TRUST_PROXY_HTTPS=True
```

Generate the secret:

```bash
python -c 'import secrets; print(secrets.token_urlsafe(48))'
```

Use TRUST_PROXY_HTTPS=True only if the hosting provider strips/replaces incoming
X-Forwarded-Proto and sets it from the real HTTPS connection. Otherwise leave it
False. Public frontend and API URLs must use HTTPS. Allowed hosts are hostnames;
CORS and CSRF origins include the scheme. Comma-separate multiple values.
Production settings always use PostgreSQL and DEBUG=False.

With repository root as the working directory, build/release commands are:

```bash
pip install -r backend/requirements/base.txt
cd backend
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```

Start command, from `backend/`:

```bash
daphne -b 0.0.0.0 -p "${PORT:-8000}" stack_underflow.asgi:application
```

Use the host's PORT value. WhiteNoise serves collected admin/static files. Create
an admin account once through the web service shell using `python manage.py
createsuperuser`. Check `/api/questions/list`, `/api/docs/` and `/admin/`.

The existing backend Dockerfile also works for a container web service:

```bash
docker build -t stack-underflow-backend ./backend
```

Supply the same environment privately to the container. Run migrations as a
release command before receiving traffic. Its default command collects static
files and starts Daphne on PORT. Do not put backend/.env into the image.

## Frontend

From `frontend/`:

```bash
npm ci
npm run build
STACK_UNDERFLOW_API_URL=https://api.your-domain.example/api npm run configure:api
```

Publish `frontend/dist/stack-underflow` on the static host. Configure an SPA
fallback: unknown frontend paths such as `/questions/example` must serve
`index.html`. Do not rewrite files that actually exist.

The public runtime setting is in `assets/config.js`; it contains only the API URL.
Changing it does not require rebuilding JavaScript. Serve this file with a short
cache lifetime or no-cache. Production defaults to `/api` if frontend and API
share an origin; a separate API host needs the command above. Development uses
http://127.0.0.1:8000/api unless src/assets/config.js overrides it.

## Verify after deployment

1. Open the frontend in a new tab. Register and log in.
2. Create a question tagged python. Reload its detail page.
3. Search by title and python; click a suggestion and add a comment.
4. Check that requests go to the deployed API, with no localhost URLs.
5. In admin, inspect AnalyticsEvent search/view/creation records and session IDs.
6. Run docs/analytics_queries.sql against the managed PostgreSQL database.

No public URL is claimed until these steps have run on the actual host.
