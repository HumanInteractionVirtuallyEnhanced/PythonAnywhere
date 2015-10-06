from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
notification = Table('notification', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user1_id', Integer),
    Column('user2_id', Integer),
    Column('comment_id', Integer),
    Column('reply_id', Integer),
    Column('typeNum', Integer, default=ColumnDefault(1)),
    Column('atTime', DateTime),
    Column('latLon', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['notification'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['notification'].drop()
