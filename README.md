# Discography App

A Flask web app for cataloguing a record collection — songs, disks, the people
who made them, the companies that released them, and disk labels. It supports
full CRUD, paginated/sortable listings, and search across entities (including
related fields, e.g. finding a song by its artist).

## Stack

- **Flask** + **Flask-SQLAlchemy** (SQLAlchemy 2.x)
- **PostgreSQL** (uses `pg_trgm` for fast substring search)
- **Flask-Migrate** (Alembic) for schema migrations
- **Flask-WTF** for forms/CSRF, **Bootstrap 5** for the UI

## Requirements

- Python 3.11+
- PostgreSQL 13+

## Setup

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Database configuration

Database settings are read from environment files in `app/env-files/`. Create
the one for your environment (these are git-ignored / machine-specific):

`app/env-files/db.env.development`
```env
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=discography
```

- **Development** loads `db.env.<FLASK_ENV>` (falling back to `db.env`).
- **Production** loads `db.env.production`, or you can set a single
  `DATABASE_URL`. It also **requires** a real `SECRET_KEY` (see below).

### Apply migrations

The schema is owned by Alembic migrations — `db.create_all()` is intentionally
not used. Run migrations before first launch and after every pull:

```bash
flask db upgrade
```

(`flask` picks up the app via `FLASK_APP=run-dev.py` or the factory; if needed,
`export FLASK_APP=run-dev.py`.)

## Running

Development (debug, auto-reload, port 5000):
```bash
python run-dev.py
```

Production (port 9292) — requires a strong secret key:
```bash
export FLASK_ENV=production
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
flask db upgrade
python run-prod.py
```

If `SECRET_KEY` is missing or left at the default, the production app refuses to
start.

## Tests

The suite uses an in-memory SQLite database, so no PostgreSQL is needed to run it:

```bash
python -m unittest discover -p 'test_*.py'
```

## Project layout

```
app/
  __init__.py          # app factory (config selection, error handlers)
  routes.py            # all views (listings, search, CRUD)
  models/              # SQLAlchemy models
  forms/               # WTForms
  templates/           # Jinja templates (partials, single_pages, errors, ...)
  env-files/           # per-environment DB settings (not committed)
config.py              # Config classes + get_config()
migrations/            # Alembic migrations
run-dev.py / run-prod.py
test_*.py              # unittest suites
```

## Migrations cheatsheet

```bash
flask db migrate -m "describe change"   # autogenerate from model changes
flask db upgrade                        # apply
flask db downgrade -1                   # roll back one
flask db current                        # show current revision
```
