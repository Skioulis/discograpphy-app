import sqlalchemy as sa
from .db import db

discsongs = db.Table(
    'discsongs',
    db.Column('dicsid', sa.Integer, sa.ForeignKey('disks.disk_id'), primary_key=True),
    db.Column('songid', sa.Integer, sa.ForeignKey('songs.id'), primary_key=True)
)