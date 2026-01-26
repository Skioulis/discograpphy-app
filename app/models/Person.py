from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db

class Person(db.Model):
    __tablename__ = 'people'

    person_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(250), index=True)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.TEXT(), nullable=True)