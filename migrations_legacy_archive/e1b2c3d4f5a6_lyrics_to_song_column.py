"""move lyrics into a songs.lyrics column and drop the lyrics table

Each song had 0 or 1 lyric row in practice; collapse any rows into a single
text column on songs (joining multiple with blank lines, just in case).

Revision ID: e1b2c3d4f5a6
Revises: d7a2f9c61b85
Create Date: 2026-06-14 20:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1b2c3d4f5a6'
down_revision = 'd7a2f9c61b85'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('songs', sa.Column('lyrics', sa.Text(), nullable=True))
    op.execute(
        "UPDATE songs SET lyrics = sub.txt FROM ("
        "SELECT song_id, string_agg(lyric, E'\\n\\n') AS txt FROM lyrics GROUP BY song_id"
        ") sub WHERE songs.song_id = sub.song_id"
    )
    op.drop_table('lyrics')


def downgrade():
    op.create_table(
        'lyrics',
        sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column('lyric', sa.Text(), nullable=False),
        sa.Column('song_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['song_id'], ['songs.song_id']),
        sa.PrimaryKeyConstraint('id', name='pk_lyrics'),
    )
    op.create_index('ix_lyrics_song_id', 'lyrics', ['song_id'])
    op.execute(
        "INSERT INTO lyrics (lyric, song_id) "
        "SELECT lyrics, song_id FROM songs WHERE lyrics IS NOT NULL"
    )
    op.drop_column('songs', 'lyrics')
