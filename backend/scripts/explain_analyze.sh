#!/bin/bash
# US-08: measure the question search queries before/after the index migrations.
# Usage (from anywhere):  backend/scripts/explain_analyze.sh
#   LOCAL_BACKEND=1 backend/scripts/explain_analyze.sh
#     -> only the Postgres container runs in Docker; Django runs from the
#        active virtualenv (no backend image build, much faster first run).
# Output: docs/explain_output/before.md and docs/explain_output/after.md
set -euo pipefail
cd "$(dirname "$0")/../.."

DC="docker compose --env-file backend/.env"
OUT=docs/explain_output
mkdir -p "$OUT"

if [ "${LOCAL_BACKEND:-0}" = "1" ]; then
  echo "Starting db (Django runs from the local virtualenv)"
  $DC up -d --wait db
  # decouple reads backend/.env itself; only point it at the published port.
  manage() { (cd backend && DB_HOST=127.0.0.1 DB_PORT="${DB_LOCAL_PORT:-5432}" python manage.py "$@"); }
else
  echo "Starting db + backend"
  $DC up -d --build db backend
  manage() { $DC exec -T backend python manage.py "$@"; }
fi
manage migrate --noinput

echo "Seeding ~5,000 questions"
manage seed_bulk --flush --count 5000

echo "BEFORE: rolling back the US-08 index migrations"
# Unapplies tags.0002 and its dependents questions.0005 + comments.0003.
manage migrate tags 0001 --noinput
$DC exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c ANALYZE' >/dev/null
manage explain_search > "$OUT/before.md"

echo "AFTER: applying the index migrations"
manage migrate --noinput
$DC exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c ANALYZE' >/dev/null
manage explain_search > "$OUT/after.md"

echo
for f in before after; do
  echo "== $f =="
  grep -E '^### |execution time' "$OUT/$f.md"
done
echo "Full plans: $OUT/before.md, $OUT/after.md"
