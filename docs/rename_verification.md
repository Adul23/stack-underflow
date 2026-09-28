# Rename verification

The standalone project uses `backend/stack_underflow/`, `frontend/` and a root
`docker-compose.yml`. See [source reference](source_reference.md) for the old
paths and original remote. That is the only file retaining the old project name.

- Python configuration package: `stack_underflow`. Imports, manage.py, pytest,
  WSGI, ASGI and Celery entry points use this name.
- Angular workspace, package, lockfile root, output and coverage names:
  `stack-underflow`.
- Existing logo asset filenames use `stack-underflow`.
- Docker services: backend, db, redis and celery_worker. Explicit containers use
  the `stack-underflow-` prefix. Paths point to backend/ and its private .env.
- Settings variables use `STACK_UNDERFLOW`. Secrets come from the environment.
- Database tables, app labels and migration contents were preserved.

## Checks completed

- `python manage.py check`: no issues.
- `python manage.py makemigrations --check --dry-run`: no changes.
- `python manage.py migrate`: all migrations applied to a fresh local SQLite DB.
- Existing API tests plus MVP tests: 77 passed.
- WSGI, ASGI and Celery imports: passed.
- Django runserver startup and GET /api/questions/list: passed.
- `npm run build`: passed. Existing bundle/component size and CSS warnings remain.
- Angular root-component tests in headless Chrome: 3 passed. Added the missing
  test entry point and supplied a missing mock constructor dependency in an
  existing directive test so the test code could compile. Other Angular tests
  and the Redis-dependent Channels tests were not run.
- Docker Compose configuration: valid. Containers were not launched.
- Original source-file hashes: unchanged. No operations pushed to its remote.
- Private environment files, databases, dependencies and caches are ignored.

The first commit is `Initial Stack Underflow MVP` on `main`, with no remote.
GitHub CLI and an authenticated GitHub connector were unavailable. After
installing GitHub CLI, run from this project directory:

```bash
gh auth login
gh repo create stack-underflow --private --source=. --remote=origin --push
```

If that repository name already exists, stop and choose another name, for example
`stack-underflow-tsis`. Do not overwrite an existing repository or force-push.
