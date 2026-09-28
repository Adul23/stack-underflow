#!/bin/bash
set -e
cd "$(dirname "$0")/../.."

echo "Running flake8"
docker compose --env-file backend/.env exec backend flake8 apps/ stack_underflow/

echo "Checking import order with isort"
docker compose --env-file backend/.env exec backend isort --check-only --diff apps/ stack_underflow/

echo "Lint done"
