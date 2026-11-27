# Local installation

## Requirements

Git, Python 3.12, Node.js 18 with npm, Docker with Compose. Chrome is needed for browser tests. Use two terminals. Commands below assume the repository root unless stated otherwise.

```bash
git clone https://github.com/Adul23/stack-underflow.git
cd stack-underflow
cp backend/.env.example backend/.env
python3 -c 'import secrets; print(secrets.token_urlsafe(48))'
```

On Windows PowerShell use `Copy-Item backend/.env.example backend/.env` and `py -3.12` instead of `python3` if necessary. Do not overwrite an existing private `.env`. Put the generated secret in `STACK_UNDERFLOW_SECRET_KEY` and choose a private `DB_PASSWORD`. Keep the local host and CORS values in the example.

## Option A: local Django, Docker database

```bash
docker compose --env-file backend/.env up -d db
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements/base.txt
cd backend
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

On Windows create the environment with `py -3.12 -m venv .venv` and activate it with `.venv\Scripts\Activate.ps1`. The superuser is for administration and staff analytics, not ordinary registration.

## Option B: Docker backend and database

```bash
docker compose --env-file backend/.env up --build -d
docker compose --env-file backend/.env exec backend python manage.py migrate
docker compose --env-file backend/.env exec backend python manage.py createsuperuser
```

Do not run both backend options on port 8000. Compose uses `DB_HOST=db` inside the container. Redis and Celery are optional legacy services.

## Frontend (both options)

In another terminal, from the root:

```bash
cd frontend
npm ci
npm start
```

Open [the application](http://localhost:4200), [Swagger](http://127.0.0.1:8000/api/docs/) or [Django admin](http://127.0.0.1:8000/admin/).

## Demo data and verification

Docker startup can insert 12 example questions and 8 tags. Existing examples are skipped. For a local backend, run `python seed_demo.py` from `backend/` with the environment activated. Set `SEED_DEMO_DATA=False` to disable automatic seeding.

Run `python manage.py check` from `backend/` and `npm run build` from `frontend/`. The build may need internet access for Google Fonts. See the [README](../README.md) for the full test commands, [troubleshooting](troubleshooting.md) for errors and [deployment](deployment.md) for production. These instructions follow the repository configuration; a fresh installation on each OS has not been verified.
