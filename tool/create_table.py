import sys
import pathlib
import psycopg2

# base.pyのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append(str(current_dir) + "/../")

import pandas as pd
import time

from estates.mydb import Mydb

db = Mydb()

try:
    # テーブルを削除
    db.drop_table_estate()

except Exception as e:
    # Tableがない場合に発生
    print("## New Estate Table")

# テーブルの作成
db.init_db()

print("## Table Estate Created ##")
