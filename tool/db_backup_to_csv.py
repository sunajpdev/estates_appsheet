import sys
import pathlib

# base.pyのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append(str(current_dir) + "/../")

import pandas as pd
import time

from estates.mydb import Mydb
from mylib.mypandas import MyPandas as mp


def main(filename):
    print("### start main ###")
    db = Mydb()
    df = pd.read_sql("select * from estates order by created", db.engine)
    df.to_csv(filename, index=False)
    print("### end main ###")


if __name__ == "__main__":

    start = time.time()
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        main(filename)
    else:
        print("Not Filename")
        exit()
    end = time.time()
    print(end - start, "s")
