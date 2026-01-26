from typing import Optional, List, TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db
from .associations import discsongs

if TYPE_CHECKING:
    from .Song import Song

class Disk(db.Model):
    __tablename__ = 'disks'

    disk_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(250), index=True)
    company: so.Mapped[Optional[str]] = so.mapped_column(sa.String(250), nullable=True)
    size: so.Mapped[Optional[str]] = so.mapped_column(sa.String(250), nullable=True)
    sakisid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(250), nullable=True)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.TEXT(), nullable=True)
    songs: so.Mapped[List['Song']] = so.relationship(
        secondary=discsongs,  # Use the object directly
        back_populates='disks'
    )
    
    def __repr__(self):
        return f'<Disk {self.name}>'