"""change disks.size from string to integer

All existing size values are numeric (e.g. 33, 45), so cast in place.

Revision ID: c4e8b1a7f230
Revises: a1f3c7d29e10
Create Date: 2026-06-14 18:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4e8b1a7f230'
down_revision = 'a1f3c7d29e10'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'disks', 'size',
        existing_type=sa.String(length=250),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using='size::integer',
    )


def downgrade():
    op.alter_column(
        'disks', 'size',
        existing_type=sa.Integer(),
        type_=sa.String(length=250),
        existing_nullable=True,
        postgresql_using='size::text',
    )
