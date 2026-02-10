from typing import Optional, List, TYPE_CHECKING
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db, TimestampMixin

if TYPE_CHECKING:
    from .Company import Company

class DiskLabel(db.Model, TimestampMixin):
    __tablename__ = 'disklabels'

    label_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    label: so.Mapped[str] = so.mapped_column(sa.TEXT(), index=True)
    company_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('companies.company_id'), index=True)

    company: so.Mapped['Company'] = so.relationship(back_populates='labels')

    def __repr__(self):
        return f'<DiskLabel {self.label}>'