#!/bin/sh
set -e

# Wait for Postgres to accept connections before doing anything DB-related.
echo "Waiting for database at ${DB_HOST}:${DB_PORT} ..."
python - <<'PY'
import os, sys, time
import psycopg2

cfg = dict(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", "5432"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME"),
)
for attempt in range(60):
    try:
        psycopg2.connect(**cfg).close()
        print("Database is ready.")
        sys.exit(0)
    except Exception as exc:
        print(f"  database not ready yet ({exc}); retrying in 2s...")
        time.sleep(2)
print("Database did not become ready in time.", file=sys.stderr)
sys.exit(1)
PY

# Apply Alembic migrations. Safe here: this is the containerised Postgres, a
# fresh volume on first run, NOT the legacy external database.
echo "Applying database migrations (flask db upgrade)..."
flask db upgrade

echo "Starting gunicorn..."
exec python run-prod.py
