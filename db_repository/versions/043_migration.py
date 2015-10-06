from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
message = Table('message', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=500)),
    Column('author_id', INTEGER),
    Column('reciever_id', INTEGER),
    Column('latLon', VARCHAR),
    Column('atTime', DATETIME),
)

message = Table('message', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=500, convert_unicode=True)),
    Column('user_id', Integer),
    Column('reciever_id', Integer),
    Column('latLon', String),
    Column('atTime', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['message'].columns['author_id'].drop()
    post_meta.tables['message'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['message'].columns['author_id'].create()
    post_meta.tables['message'].columns['user_id'].drop()
