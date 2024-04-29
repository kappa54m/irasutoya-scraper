from irasutoya.utils import getenv

from sqlalchemy import create_engine, Column, Table, MetaData
from sqlalchemy import Integer, String, Date, DateTime, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os


Base = declarative_base()
__db_engine = None


def get_db_engine():
    """
    Return a globally cached db engine (from DB_CONNECTION_STRING envvar) after creating one if it does not already exist.
    """
    global __db_engine
    if __db_engine is not None:
        return __db_engine
    else:
        print("Global db engine has not been initialized. Initializing...")
        __db_engine = db_init()
        return __db_engine


def db_init(conn_str=None):
    """
    Instantiate and return a new database engine backed by SQLAlchemy.
    If conn_str is not provided, it will use the DB_CONNECTION_STRING environment variable instead.
    """
    if conn_str is None:
        conn_str = getenv('DB_CONNECTION_STRING', None)
    if not conn_str:
        raise Exception("'DB_CONNECTION_STRING' environment variable not found.")
    else:
        db_engine = create_engine(conn_str)
        Base.metadata.create_all(db_engine)
        print("Initialized database engine")
        return db_engine


class IrasutoyaIrasuto(Base):
    __tablename__ = 'irasutoya_irasuto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text)
    description = Column(Text)
    entry_raw = Column(Text)
    tags = Column(Text)
    upload_date = Column(Text)
    images_download_info = Column(Text)

    scraped_datetime = Column(DateTime)
