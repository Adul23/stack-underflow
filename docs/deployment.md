# Deploy the MVP

Architecture: static Angular frontend → Django REST API → PostgreSQL.
Redis, Celery and WebSockets are not required for this flow. The old optional
Docker services can be started with `--profile legacy` if needed separately.

The production backend is configured for Render. Repository changes must be
deployed to the existing service before they affect its PostgreSQL database.
The instructions below cover both Docker and Render's native Python runtime.

## Backend environment

Set these in the web service's private environment; never commit them:

```dotenv
STACK_UNDERFLOW_ENV_ID=prod
STACK_UNDERFLOW_SECRET_KEY=<random secret generated locally>
ALLOWED_HOSTS=api.your-domain.example
CORS_ALLOWED_ORIGINS=https://your-frontend.example
CSRF_TRUSTED_ORIGINS=https://api.your-domain.example
DATABASE_URL=<Render PostgreSQL internal connection URL>
SEED_DEMO_DATA=True
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
python start.py
```

Use the host's PORT value. WhiteNoise serves collected admin/static files. Create
an admin account once through the web service shell using `python manage.py
createsuperuser`. Check `/api/questions/list`, `/api/docs/` and `/admin/`.

The existing backend Dockerfile also works for a container web service:

```bash
docker build -t stack-underflow-backend ./backend
```

Supply the same environment privately to the container. Its default command is
`python start.py`: apply migrations, run `seed_demo.py`, collect static files,
then start Daphne on PORT. A failed preparation step prevents the server from
starting. Do not put backend/.env into the image.

## Automatic demo data on Docker and Render

`backend/seed_demo.py` adds 12 programming questions, 8 tags and their links.
It creates a Demo Author account with an unusable password and no admin rights;
register normally to publish your own questions. It does not require a seed
password, delete existing data, reset passwords or create fake analytics events.

Stable demo slugs make repeated runs skip existing questions. Existing content,
tag associations and soft-deleted questions are preserved. If you rename a demo
question through the API, its slug changes; the original example can then be
created again on the next seed. All inserts use one transaction; simultaneous
PostgreSQL runs use an advisory lock. A partial failure rolls back the inserts.
Set `SEED_DEMO_DATA=False` to skip automatic seeding while keeping existing rows.

On **Render Docker**, use `backend/Dockerfile` with `backend` as the Docker build
context (or set Root Directory to `backend` and Dockerfile Path to `Dockerfile`).
Leave Docker Command empty to use the Dockerfile CMD, or set it to
`python start.py`. An existing custom Docker Command takes precedence over CMD.
See [Render Docker configuration](https://render.com/docs/docker).

On **Render Python**, with Root Directory `backend`, set Build Command to
`pip install -r requirements/base.txt` and Start Command to `python start.py`.
With the repository root as Root Directory, use
`pip install -r backend/requirements/base.txt` and `python backend/start.py`.
Set `STACK_UNDERFLOW_ENV_ID=prod` and the existing private `DATABASE_URL` so
the examples are inserted into the Render PostgreSQL database.

Deploy these changes to the branch connected to the Render service. Every
subsequent backend start runs the seed automatically. Opening Docker Desktop
locally does not restart the service on Render.

For **local Docker**, after configuring `backend/.env`, run:

```bash
docker compose --env-file backend/.env up --build -d
```

The backend and database use `restart: unless-stopped`, so already-running
containers return after a Docker restart unless explicitly stopped. The local
database stays in the `db_data` volume. Local Compose uses `DB_HOST=db` and
the local database credentials, separately from the Render database.

To add examples manually using the current Django database configuration:

```bash
cd backend
python seed_demo.py
```

Or run `backend/scripts/seed.sh` against the local Compose backend. Check the
startup log for `Demo data ready` and `/api/questions/list` for the examples.

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
