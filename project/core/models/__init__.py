from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import redis

from project.config import MYSQL_DB_URL

engine = create_engine(
    MYSQL_DB_URL,
    encoding="utf-8",
    pool_recycle=3600,
    pool_size=20,
    max_overflow=20,
    pool_pre_ping=True,
    echo=True
)

Base = declarative_base()

Session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
session = Session()

Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
