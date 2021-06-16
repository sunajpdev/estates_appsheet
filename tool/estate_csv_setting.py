import sys
import pathlib

# base.pyのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append(str(current_dir) + "/../")


import pandas as pd
import numpy as np

from mylib.address import Address
from mylib.mypandas import MyPandas as mp


import pandas as pd
import time


def main(input_csv, output_csv):

    print("### start main ###")

    df = pd.read_csv(input_csv)
    rows = df.to_dict(orient="records")

    for index, row in enumerate(rows):
        if row["prefecture"] is np.nan:
            print(row)
            prefecture, city = Address.address_to_prefecture_and_city(row["place"])
            rows[index]["prefecture"] = prefecture
            print("## NEW ##", row)

    mp.to_csv(rows, output_csv)

    print("### end main ###")


if __name__ == "__main__":

    start = time.time()
    if len(sys.argv) == 3:
        input_csv = sys.argv[1]
        output_csv = sys.argv[2]
        main(input_csv, output_csv)
    else:
        print("Not Filename")
        exit()
    end = time.time()
    print(end - start, "s")
