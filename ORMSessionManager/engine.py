"""
Connecting to MySQL localhost by default, change connection to use different DB.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Database settings
DATABASE_HOSTNAME = 'localhost'
DATABASE_USERNAME = 'root'
DATABASE_PASSWORD = 'root'
DATABASE_SCHEMA = 'UWT'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{passwd}@{host}/{schema}?charset=utf8'.format(host=DATABASE_HOSTNAME, user=DATABASE_USERNAME, passwd=DATABASE_PASSWORD, schema=DATABASE_SCHEMA)

# Engine
ENGINE = create_engine(SQLALCHEMY_DATABASE_URI)
FACTORY = sessionmaker(bind=ENGINE)
SESSION = scoped_session(FACTORY)
