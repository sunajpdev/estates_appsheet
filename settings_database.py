# from settings import ReadIni

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


import pandas as pd

Base = declarative_base()
engine = create_engine(
    "postgresql://postgres:hoge@localhost/estates_appsheet", echo=False
)

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = session.query_property()


def init_db():
    from estates import models

    Base.metadata.create_all(bind=engine)
