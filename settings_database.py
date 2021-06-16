# from settings import ReadIni

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


import pandas as pd

from settings import ReadIni as ri

database = ri.ini.get("DB", "database")
user = ri.ini.get("DB", "user")
password = ri.ini.get("DB", "password")
host = ri.ini.get("DB", "host")
dbname = ri.ini.get("DB", "dbname")

uri = f"{database}://{user}:{password}@{host}/{dbname}"

Base = declarative_base()
engine = create_engine(uri, echo=False)

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = session.query_property()
mate = Base.metadata


def init_db():
    from estates import models

    # Base.metadata.create_all(bind=engine)
    mate.create_all(bind=engine)
