from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
hashtag = Table('hashtag', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=120)),
)

hashtagOwners = Table('hashtagOwners', post_meta,
    Column('hash_id', Integer),
    Column('user_id', Integer),
)

strong_hashtag_connection = Table('strong_hashtag_connection', post_meta,
    Column('parent_id', Integer),
    Column('child_id', Integer),
)

weak_hashtag_connection = Table('weak_hashtag_connection', post_meta,
    Column('parent_id', Integer),
    Column('child_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['hashtag'].create()
    post_meta.tables['hashtagOwners'].create()
    post_meta.tables['strong_hashtag_connection'].create()
    post_meta.tables['weak_hashtag_connection'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['hashtag'].drop()
    post_meta.tables['hashtagOwners'].drop()
    post_meta.tables['strong_hashtag_connection'].drop()
    post_meta.tables['weak_hashtag_connection'].drop()
