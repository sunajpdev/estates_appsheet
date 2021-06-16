import sys
import pathlib

# base.pyのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append(str(current_dir) + "/../")

import pandas as pd
import time

from estates.mydb import Mydb, Estate, session

db = Mydb()


def insert_estate_all_commit(estates_dict_rows):
    """顧客dictを渡したらまとめてInsertしてCommit。
    失敗時はDBにはcommitせずに終了
    成功時: True
    失敗時: False"""

    for row in estates_dict_rows:
        estate = Estate(**row)
        session.add(estate)

    try:
        session.commit()
        result = True
    except Exception as e:
        print("# ERROR insert_estate_all_commit #", e)
        session.rollback()
        result = False

    return result


def main(filename):

    print("### start main ###")
    df = pd.read_csv(filename)

    rows = df.to_dict(orient="records")

    res = insert_estate_all_commit(rows)

    if res:
        print("Success.")
    else:
        print("Error")


if __name__ == "__main__":

    start = time.time()
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        res = input(f"Database Restore {filename} [y/n]")
        if res == "y":
            main(filename)
        else:
            print("Cancel.")
    else:
        print("Not Filename")
        exit()
    end = time.time()
    print(end - start, "s")
