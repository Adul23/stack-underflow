#!/bin/bash
set -e
cd "$(dirname "$0")/../.."

echo "Making migrations"
docker compose --env-file backend/.env exec backend python manage.py makemigrations

echo "Applying migrations"
docker compose --env-file backend/.env exec backend python manage.py migrate

echo "Done."
