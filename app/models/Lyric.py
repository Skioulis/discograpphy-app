from typing import Optional, TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db

if TYPE_CHECKING:
    from .Song import Song

class Lyric(db.Model):
    __tablename__ = 'lyrics'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    lyric: so.Mapped[str] = so.mapped_column(sa.Text)
    song_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('songs.id'), index=True)

    song: so.Mapped['Song'] = so.relationship(back_populates='lyrics')

    def __repr__(self):
        return f'<Lyric {self.id} for Song {self.song_id}>'
