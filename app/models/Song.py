from typing import List, Optional, TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db, TimestampMixin

if TYPE_CHECKING:
    from .Lyric import Lyric
    from .associations import PersonSongRole


class Song(db.Model, TimestampMixin):
    __tablename__ = 'songs'

    song_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(250), index=True)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)

    lyrics: so.Mapped[List['Lyric']] = so.relationship(
        back_populates='song', cascade='all, delete-orphan'
    )

    person_roles: so.Mapped[List['PersonSongRole']] = so.relationship(
        back_populates='song', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Song {self.song_id} {self.title!r}>'
