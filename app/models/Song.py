from typing import List, Optional, TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

if TYPE_CHECKING:
    from .Lyric import Lyric

class Song(db.Model):
    __tablename__ = 'songs'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(250), index=True)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.TEXT(), nullable=True)

    lyrics: so.Mapped[List['Lyric']] = so.relationship(back_populates='song', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Song {self.title}>'
    