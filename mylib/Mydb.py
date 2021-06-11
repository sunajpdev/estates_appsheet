import configparser

ini = configparser.ConfigParser()
ini.read("config.ini", encoding="utf-8")

from sqlalchemy import create_engine, text


class Mydb:
    def __init__(self):
        database, user, password, host, dbname = (
            ini.get("DB", "database"),
            ini.get("DB", "user"),
            ini.get("DB", "password"),
            ini.get("DB", "host"),
            ini.get("DB", "dbname"),
        )
        url = f"{database}://{user}:{password}@{host}/{dbname}"
        self.engine = create_engine(url)

    def return_true(self):
        return True
