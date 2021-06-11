import configparser

ini = configparser.ConfigParser()
ini.read("config.ini", encoding="utf-8")

import pandas as pd
import time

from mylib.Mydb import Mydb


start = time.time()

df = pd.read_csv("tmp/_gs.csv")

rows = df.to_dict(orient="records")

db = Mydb()

for row in rows:
    res = db.insert_estate(row)
    if res != True:
        print("[ERROR]:", row)
        print(res)

end = time.time()
print(end - start, "s")
