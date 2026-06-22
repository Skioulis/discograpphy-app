"""add audio_path and image_path to songs

Adds two optional file-path columns to the songs table: audio_path (mp3) and
image_path. Paths point at files under the media bind mount.

Revision ID: b3d1a7c95e02
Revises: e0f0808b9f6a
Create Date: 2026-06-22 19:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3d1a7c95e02'
down_revision = 'e0f0808b9f6a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('audio_path', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('image_path', sa.String(length=500), nullable=True))


def downgrade():
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.drop_column('image_path')
        batch_op.drop_column('audio_path')
