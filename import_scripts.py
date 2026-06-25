"""One-off data imports.

import_people_names: load the names from column 2 ("c2") of
data/peopletofix.csv into the `people` table. IDs are auto-generated;
blank names, in-file duplicate names, and names already present are skipped
(the table has a unique constraint on `name`). Idempotent — safe to re-run.

Usage (against the apollon-dev database):
    FLASK_ENV=development .venv/bin/python import_scripts.py

Against any other database, set DATABASE_URL (overrides the env-file config):
    DATABASE_URL="postgresql://user:pass@host:5432/dbname" \
        .venv/bin/python import_scripts.py
"""
import csv
import os

from app import create_app
from config import DevelopmentConfig
from app.models.db import db
from app.models.Person import Person

CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'peopletofix.csv')
NAME_COLUMN = 1  # 0-indexed; column 2 ("c2") in the CSV


def import_people_names(csv_path=CSV_PATH):
    existing = {name for (name,) in db.session.query(Person.name)}
    seen = set(existing)

    to_add = []
    skipped_blank = skipped_dup = 0
    with open(csv_path, newline='', encoding='utf-8') as fh:
        for row in csv.reader(fh):
            if len(row) <= NAME_COLUMN:
                continue
            name = row[NAME_COLUMN].strip()
            if not name:
                skipped_blank += 1
                continue
            if name in seen:
                skipped_dup += 1
                continue
            seen.add(name)
            to_add.append(Person(name=name))

    db.session.add_all(to_add)
    db.session.commit()

    print(f'Inserted {len(to_add)} people.')
    print(f'Skipped {skipped_blank} blank names, {skipped_dup} duplicate/existing names.')


if __name__ == '__main__':
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Point the app at an arbitrary database without editing env files.
        DevelopmentConfig.database_uri = database_url
        app = create_app(DevelopmentConfig)
    else:
        app = create_app()
    with app.app_context():
        print(f'Target DB: {app.config["SQLALCHEMY_DATABASE_URI"]}')
        import_people_names()
