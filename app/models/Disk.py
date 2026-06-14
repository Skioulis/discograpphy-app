from typing import Optional, List, TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so

from .db import db, TimestampMixin
from .associations import discsongs

if TYPE_CHECKING:
    from .Song import Song
    from .Company import Company

class Disk(db.Model, TimestampMixin):
    __tablename__ = 'disks'
    __table_args__ = (
        sa.UniqueConstraint('name', name='uq_disks_name'),
    )

    disk_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(250), index=True)
    size: so.Mapped[Optional[int]] = so.mapped_column(nullable=True)
    sakisid: so.Mapped[Optional[str]] = so.mapped_column(sa.String(250), nullable=True)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.TEXT(), nullable=True)

    company_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('companies.company_id'), index=True)

    company: so.Mapped['Company'] = so.relationship(back_populates='disks')

    songs: so.Mapped[List['Song']] = so.relationship(
        secondary=discsongs,  # Use the object directly
        back_populates='disks'
    )
    
    def __repr__(self):
        return f'<Disk {self.name}>'