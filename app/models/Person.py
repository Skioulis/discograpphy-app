from typing import List, Optional, TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db, TimestampMixin

if TYPE_CHECKING:
    from .associations import PersonSongRole


class Person(db.Model, TimestampMixin):
    __tablename__ = 'people'

    person_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(250), index=True)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)

    song_roles: so.Mapped[List['PersonSongRole']] = so.relationship(
        back_populates='person', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Person {self.person_id} {self.name!r}>'
