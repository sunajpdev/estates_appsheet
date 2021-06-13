import configparser

import pandas as pd

ini = configparser.ConfigParser()
ini.read("config.ini", encoding="utf-8")

from sqlalchemy import create_engine, text, exc
from settings import ReadIni


class Mydb:
    def __init__(self):
        """クラス生成時にDBに接続するengineを追加"""

        cf = ReadIni()

        database, user, password, host, dbname = (
            cf.ini.get("DB", "database"),
            cf.ini.get("DB", "user"),
            cf.ini.get("DB", "password"),
            cf.ini.get("DB", "host"),
            cf.ini.get("DB", "dbname"),
        )
        url = f"{database}://{user}:{password}@{host}/{dbname}"
        self.engine = create_engine(url)
        self.text = text

    def record_count(self, table, id):
        """レコードの有無をチェックする"""

        sql = self.text(f"SELECT * FROM {table} WHERE id=:id")
        res = self.engine.execute(sql, id=id)
        cnt = len(list(res))
        return cnt

    def delete_estate(self, id):
        """指定idのestateを削除 成功:True 失敗:エラー情報"""

        sql = self.text("DELETE FROM estates WHERE id=:id;")
        try:
            self.engine.execute(sql, id=id)
            return True
        except Exception as e:
            print(e)
            return False

    def insert_estate_new_data(self, estate_dict):
        """データが重複していない場合のみ insert_estateを実行
        成功時: id
        失敗時: False
        """

        id = estate_dict["id"]
        cnt = self.record_count("estates", id)
        if cnt == 0:
            res = self.insert_estate(estate_dict)
            return res
        else:
            return False

    def insert_estate(self, estate_dict):
        """顧客dictを渡したらINSERT SQLを生成して実行。
        成功時: id
        失敗時: False"""

        sql = self.text(
            "\
            INSERT INTO estates( \
                id, note, price, shop, place, prefecture, city, station, route, work, area, \
                buildingarea, ldk, buildingyear, url) \
            VALUES( \
                :id, :note, :price, :shop, :place, :prefecture, :city, :station, :route, :work, :area,\
                :buildingarea, :ldk, :buildingyear, :url) \
            "
        )

        try:
            self.engine.execute(sql, estate_dict)
            result = estate_dict["id"]
        except exc.IntegrityError as ie:
            # TODO: add logger
            result = False

        return result

    def all_estate_to_csv(self, filename):
        """DBからすべてのEstateを取得してCSVに保存する"""

        sql = "SELECT * from estates ORDER BY created"
        df = pd.read_sql(sql, self.engine)
        df.to_csv(filename, index=False)

        return filename
