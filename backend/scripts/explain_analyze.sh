#!/bin/bash
# US-08: measure the question search queries before/after the index migrations.
# Usage (from anywhere):  backend/scripts/explain_analyze.sh
# Output: docs/explain_output/before.md and docs/explain_output/after.md
set -euo pipefail
cd "$(dirname "$0")/../.."

DC="docker compose --env-file backend/.env"
OUT=docs/explain_output
mkdir -p "$OUT"

echo "Starting db + backend"
$DC up -d --build db backend
$DC exec -T backend python manage.py migrate --noinput

echo "Seeding ~5,000 questions"
$DC exec -T backend python manage.py seed_bulk --flush --count 5000

echo "BEFORE: rolling back the US-08 index migrations"
# Unapplies tags.0002 and its dependents questions.0005 + comments.0003.
$DC exec -T backend python manage.py migrate tags 0001 --noinput
$DC exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c ANALYZE' >/dev/null
$DC exec -T backend python manage.py explain_search > "$OUT/before.md"

echo "AFTER: applying the index migrations"
$DC exec -T backend python manage.py migrate --noinput
$DC exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c ANALYZE' >/dev/null
$DC exec -T backend python manage.py explain_search > "$OUT/after.md"

echo
for f in before after; do
  echo "== $f =="
  grep -E '^### |execution time' "$OUT/$f.md"
done
echo "Full plans: $OUT/before.md, $OUT/after.md"
