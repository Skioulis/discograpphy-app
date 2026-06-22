"""add pg_trgm GIN indexes for fast ILIKE substring search

Speeds up the contains-search ('%term%') used by /search as the collection
grows; a plain btree index can't serve leading-wildcard ILIKE.

Revision ID: a8d3e0f12c47
Revises: f6a5b4c3d2e1
Create Date: 2026-06-14 20:40:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'a8d3e0f12c47'
down_revision = 'f6a5b4c3d2e1'
branch_labels = None
depends_on = None

# (index name, table, column) for every column searched with ILIKE.
INDEXES = [
    ('ix_trgm_songs_title', 'songs', 'title'),
    ('ix_trgm_songs_notes', 'songs', 'notes'),
    ('ix_trgm_disks_name', 'disks', 'name'),
    ('ix_trgm_disks_notes', 'disks', 'notes'),
    ('ix_trgm_disks_sakisid', 'disks', 'sakisid'),
    ('ix_trgm_people_name', 'people', 'name'),
    ('ix_trgm_people_notes', 'people', 'notes'),
    ('ix_trgm_companies_name', 'companies', 'name'),
    ('ix_trgm_companies_info', 'companies', 'info'),
    ('ix_trgm_disklabels_label', 'disklabels', 'label'),
]


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
    for name, table, column in INDEXES:
        op.execute(
            f'CREATE INDEX IF NOT EXISTS {name} ON {table} '
            f'USING gin ({column} gin_trgm_ops)'
        )


def downgrade():
    for name, _table, _column in INDEXES:
        op.execute(f'DROP INDEX IF EXISTS {name}')
    # Leave the pg_trgm extension in place; other objects may rely on it.
