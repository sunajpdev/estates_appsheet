import configparser

ini = configparser.ConfigParser()
ini.read("config.ini", encoding="utf-8")

from sqlalchemy import create_engine, text
from mylib.MyConfig import MyConfig


class Mydb:
    def __init__(self):
        """ クラス生成時にDBに接続するengineを追加 """

        cf = MyConfig()

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

    def insert_estate(self, estate_dict):
        """ 顧客dictを渡したらINSERT SQLを生成して実行。成功時True 失敗時はエラー情報"""

        sql = self.text(
            "\
            INSERT INTO estates( \
                id, note, price, shop, place, prefecture, city, station, route, work, area, \
                buildingarea, ldk, buildingyear, url) \
            VALUES( \
                :id, :note, :price, :shop, :place, :prefecture, :city, :station, :route, :work, :area,\
                :buildingarea, :ldk, :buildingyear, :url) \
             ON CONFLICT DO NOTHING;\
            "
        )

        try:
            self.engine.execute(sql, estate_dict)
            result = estate_dict["id"]
        except Exception as e:
            print(e)
            return False

        return result

    def delete_estate(self, id):
        """ 指定idのestateを削除 成功:True 失敗:エラー情報"""

        sql = self.text("DELETE FROM estates WHERE id=:id;")
        try:
            self.engine.execute(sql, id=id)
            return True
        except Exception as e:
            print(e)
            return False
