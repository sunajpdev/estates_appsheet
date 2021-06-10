import configparser

ini = configparser.ConfigParser()
ini.read("config.ini", encoding="utf-8")

from sqlalchemy import create_engine, text

database, user, password, host, dbname = (
    ini.get("DB", "database"),
    ini.get("DB", "user"),
    ini.get("DB", "password"),
    ini.get("DB", "host"),
    ini.get("DB", "dbname"),
)
url = f"{database}://{user}:{password}@{host}/{dbname}"

engine = create_engine(url)
conn = engine.connect().connection
