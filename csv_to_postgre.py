import configparser

ini = configparser.ConfigParser()
ini.read("config.ini", encoding="utf-8")

import pandas as pd
import time

from mylib import Mydb


start = time.time()

df = pd.read_csv("tmp/_gs.csv")

rows = df.to_dict(orient="records")

db = Mydb.Mydb()

sql = db.text(
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
        db.engine.execute(sql, row)
    except Exception as e:
        print("[SKIP]", e)

end = time.time()
print(end - start, "s")
