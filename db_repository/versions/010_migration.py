from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
comment = Table('comment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=500, convert_unicode=True)),
    Column('user_id', Integer),
    Column('atTime', DateTime),
    Column('parent_id', Integer),
    Column('depth', Integer, default=ColumnDefault(1)),
    Column('latLon', String),
    Column('locationAddress', String),
    Column('imgLink', String),
    Column('bodyUni', Unicode),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comment'].columns['bodyUni'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comment'].columns['bodyUni'].drop()
