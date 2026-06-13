from typing import TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db

if TYPE_CHECKING:
    from .Person import Person
    from .Song import Song


class PersonSongRole(db.Model):
    """Association object linking a Person to a Song, carrying role flags.

    One row per (person, song) pair; the booleans say what that person did
    on that song.
    """
    __tablename__ = 'person_song_roles'

    person_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('people.person_id'), primary_key=True
    )
    song_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('songs.song_id'), primary_key=True
    )

    isComposer: so.Mapped[bool] = so.mapped_column(default=False)
    isSongwriter: so.Mapped[bool] = so.mapped_column(default=False)
    isSinger: so.Mapped[bool] = so.mapped_column(default=False)
    isMusician: so.Mapped[bool] = so.mapped_column(default=False)

    person: so.Mapped['Person'] = so.relationship(back_populates='song_roles')
    song: so.Mapped['Song'] = so.relationship(back_populates='person_roles')

    def roles(self):
        names = []
        if self.isComposer:
            names.append('Composer')
        if self.isSongwriter:
            names.append('Songwriter')
        if self.isSinger:
            names.append('Singer')
        if self.isMusician:
            names.append('Musician')
        return names

    def __repr__(self):
        return f'<PersonSongRole person={self.person_id} song={self.song_id} {self.roles()}>'
