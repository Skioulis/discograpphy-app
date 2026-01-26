from typing import Optional, List, TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db

if TYPE_CHECKING:
    from .associations import PeopleSong

class Person(db.Model):
    __tablename__ = 'people'

    person_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(250), index=True)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.TEXT(), nullable=True)

    songs: so.Mapped[List['PeopleSong']] = so.relationship(back_populates='person')