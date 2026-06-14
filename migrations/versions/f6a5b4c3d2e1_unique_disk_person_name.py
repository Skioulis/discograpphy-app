"""add unique constraints on disks.name and people.name

Matches the application-level uniqueness checks in DiskForm/PersonForm so
duplicates can't be created via races or direct writes.

Revision ID: f6a5b4c3d2e1
Revises: e1b2c3d4f5a6
Create Date: 2026-06-14 20:10:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'f6a5b4c3d2e1'
down_revision = 'e1b2c3d4f5a6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uq_disks_name', 'disks', ['name'])
    op.create_unique_constraint('uq_people_name', 'people', ['name'])


def downgrade():
    op.drop_constraint('uq_people_name', 'people', type_='unique')
    op.drop_constraint('uq_disks_name', 'disks', type_='unique')
