from typing import Optional, List, TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db, TimestampMixin

if TYPE_CHECKING:
    from .Disk import Disk
    from .DiskLabel import DiskLabel


class Company(db.Model, TimestampMixin):
    __tablename__ = 'companies'

    company_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(250), index=True)
    labels_size: so.Mapped[int] = so.mapped_column(default=45)
    info: so.Mapped[Optional[str]] = so.mapped_column(sa.TEXT(), nullable=True)

    disks: so.Mapped[List['Disk']] = so.relationship(back_populates='company')

    labels: so.Mapped[List['DiskLabel']] = so.relationship(back_populates='company')

    def __repr__(self):
        return f'<Company {self.name}>'
