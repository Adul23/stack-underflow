#!/bin/bash
set -e
cd "$(dirname "$0")/../.."

echo "Seeding database"
docker compose --env-file backend/.env exec backend python seed_demo.py

echo "Done."
