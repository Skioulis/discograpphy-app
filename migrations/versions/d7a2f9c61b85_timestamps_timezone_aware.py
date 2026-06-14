"""make created_at/updated_at timezone-aware (timestamptz)

Existing naive values were written as UTC, so interpret them AT TIME ZONE 'UTC'
when converting to timestamptz.

Revision ID: d7a2f9c61b85
Revises: c4e8b1a7f230
Create Date: 2026-06-14 19:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7a2f9c61b85'
down_revision = 'c4e8b1a7f230'
branch_labels = None
depends_on = None

TABLES = ['companies', 'disklabels', 'disks', 'lyrics', 'people', 'songs']
COLUMNS = ['created_at', 'updated_at']


def upgrade():
    for table in TABLES:
        for column in COLUMNS:
            op.execute(
                f'ALTER TABLE {table} ALTER COLUMN {column} '
                f"TYPE timestamptz USING {column} AT TIME ZONE 'UTC'"
            )


def downgrade():
    for table in TABLES:
        for column in COLUMNS:
            op.execute(
                f'ALTER TABLE {table} ALTER COLUMN {column} '
                f"TYPE timestamp USING {column} AT TIME ZONE 'UTC'"
            )
