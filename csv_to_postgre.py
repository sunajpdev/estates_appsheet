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


import pandas as pd
import time

start = time.time()

df = pd.read_csv("tmp/_gs.csv")

rows = df.to_dict(orient="records")

sql = text(
    "\
    INSERT INTO estates( \
        id, note, price, shop, place, prefecture, city, station, route, work, area, \
        buildingarea, ldk, buildingyear, url) \
    VALUES( \
        :id, :note, :price, :shop, :place, :prefecture, :city, :station, :route, :work, :area,\
        :buildingarea, :ldk, :buildingyear, :url) \
    "
)

for row in rows:
    try:
        engine.execute(sql, row)
    except Exception as e:
        print(e)

end = time.time()
print(end - start, "s")
