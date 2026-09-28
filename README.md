# STACK UNDERFLOW

Stack Underflow is a simple university Q&A application where users can create
questions, use tags, search existing questions and leave comments.

- Frontend: Angular
- Backend: Django REST Framework
- Database: PostgreSQL in Docker; SQLite for the local demo

## Project structure

```text
stack-underflow/
├── backend/
│   ├── manage.py
│   ├── stack_underflow/   # Django settings, URLs, ASGI, WSGI and Celery
│   └── apps/             # Users, questions, tags and comments
├── frontend/             # Angular app
├── docs/
└── docker-compose.yml
```

## Run locally

Use Python 3.12 and Node.js 18 with npm. From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements/base.txt
cp backend/.env.example backend/.env
```

Generate a secret with `python -c 'import secrets; print(secrets.token_urlsafe(48))'`
and put it after `STACK_UNDERFLOW_SECRET_KEY=` in `backend/.env`.
Keep this file private. Then:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

In another terminal, from the project root:

```bash
cd frontend
npm ci
npm start
```

Open http://localhost:4200. API: http://127.0.0.1:8000/api/docs/.
Admin: http://127.0.0.1:8000/admin/. Local SQLite needs no Redis or Celery worker.

## Run backend with PostgreSQL

Set a private `DB_PASSWORD` in `backend/.env`. From the project root:

```bash
docker compose --env-file backend/.env up --build -d
docker compose --env-file backend/.env exec backend python manage.py migrate
docker compose --env-file backend/.env exec backend python manage.py createsuperuser
```

Start Angular with `cd frontend && npm start`. Compose reuses the existing Redis
and Celery services. Its database volume belongs to this new project.
Stop any local server using ports 8000 or 6379 before starting Compose.

See [TSIS 3](docs/TSIS3.md) for the demo flow and SQL queries.
