from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
friend_requests = Table('friend_requests', post_meta,
    Column('requester_id', Integer),
    Column('requested_id', Integer),
)

friends_confirmed = Table('friends_confirmed', post_meta,
    Column('requester_id', Integer),
    Column('requested_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['friend_requests'].create()
    post_meta.tables['friends_confirmed'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['friend_requests'].drop()
    post_meta.tables['friends_confirmed'].drop()
