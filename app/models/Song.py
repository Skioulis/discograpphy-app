from typing import List, Optional, TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db, TimestampMixin
from .associations import discsongs

if TYPE_CHECKING:
    from .Disk import Disk
    from .Lyric import Lyric
    from .associations import PeopleSong

class Song(db.Model, TimestampMixin):
    __tablename__ = 'songs'

    song_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(250), index=True)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.TEXT(), nullable=True)

    lyrics: so.Mapped[List['Lyric']] = so.relationship(back_populates='song', cascade='all, delete-orphan')
    
    disks: so.Mapped[List['Disk']] = so.relationship(
        secondary=discsongs,
        back_populates='songs'
    )

    people: so.Mapped[List['PeopleSong']] = so.relationship(back_populates='song')

    def __repr__(self):
        people_details = []
        for ps in self.people:
            roles = []
            if ps.isComposer:
                roles.append('Composer')
            if ps.isSongwriter:
                roles.append('Writer')
            if ps.isSinger:
                roles.append('Singer')
            if ps.isMusician:
                roles.append('Musician')

            role_str = ', '.join(roles) if roles else 'No roles'
            people_details.append(f"{ps.person.name}: {role_str}")

        people_str = '; '.join(people_details) if people_details else 'No people'
        return f'<Song {self.title} ({people_str})>'
