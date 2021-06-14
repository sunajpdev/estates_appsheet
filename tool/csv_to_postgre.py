import sys
import pathlib

# base.pyのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append(str(current_dir) + "/../")

import pandas as pd
import time

from estates.Mydb import Mydb

start = time.time()

df = pd.read_csv("backup.csv")

rows = df.to_dict(orient="records")

db = Mydb()

for row in rows:
    res = db.insert_estate(row)
    if res != True:
        print("[ERROR]:", row)
        print(res)

end = time.time()
print(end - start, "s")
