from typing import TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db, TimestampMixin

if TYPE_CHECKING:
    from .Person import Person
    from .Song import Song

discsongs = db.Table(
    'discsongs',
    db.Column('dicsid', sa.Integer, sa.ForeignKey('disks.disk_id'), primary_key=True),
    db.Column('songid', sa.Integer, sa.ForeignKey('songs.song_id'), primary_key=True)
)

class PeopleSong(db.Model):
    __tablename__ = 'peoplesongs'

    person_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('people.person_id'), primary_key=True)
    song_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('songs.song_id'), primary_key=True)
    isComposer: so.Mapped[bool] = so.mapped_column(default=False)
    isSongwriter: so.Mapped[bool] = so.mapped_column(default=False)
    isSinger: so.Mapped[bool] = so.mapped_column(default=False)
    isMusician: so.Mapped[bool] = so.mapped_column(default=False)

    person: so.Mapped['Person'] = so.relationship(back_populates='songs')
    song: so.Mapped['Song'] = so.relationship(back_populates='people')