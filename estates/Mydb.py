import pandas as pd

from sqlalchemy import text, exc

from settings_database import session, engine, init_db

from estates.models import Estate


class Mydb:
    def __init__(self):
        """クラス生成時にDBに接続するengineを追加"""

        self.engine = engine
        self.session = session
        self.text = text

    def init_db(self):
        """Tableの作成を行う"""
        init_db()

    def drop_table_estate(self):
        """EstateTableを削除"""
        Estate.__table__.drop(engine)

    def record_count(self, model, id):
        """レコードの有無をチェックする
        あり: True
        なし: False
        """

        res = self.session.query(Estate.id).filter_by(id=id).first()

        if res != None:
            return True
        else:
            return False

    def delete_estate(self, id):
        """指定idのestateを削除 成功:True 失敗:エラー情報"""

        res = session.query(Estate).filter(Estate.id == id).delete()
        return res

    def insert_estate(self, estate_dict):
        """顧客dictを渡したらINSERT SQLを生成して実行。
        成功時: id
        失敗時: False"""

        id = estate_dict["id"]
        res_bol = self.record_count(Estate, id)

        if res_bol == False:
            try:
                estate = Estate(**estate_dict)
                session.add(estate)
                session.commit()
                result = estate.id
            except Exception as e:
                print("#ERROR insert_estate#", e)
                session.rollback()
                result = False
        else:
            result = False

        return result

    def all_estate_to_csv(self, filename):
        """DBからすべてのEstateを取得してCSVに保存する"""

        sql = "SELECT * from estates ORDER BY created"
        df = pd.read_sql(sql, self.engine)
        df.to_csv(filename, index=False)

        return filename
