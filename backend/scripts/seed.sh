#!/bin/bash
set -e
cd "$(dirname "$0")/../.."

echo "Seeding database"
docker compose --env-file backend/.env exec backend python manage.py seed --flush

echo "Done."
