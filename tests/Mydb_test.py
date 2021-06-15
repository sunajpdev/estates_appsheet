import unittest as ut
from estates.Mydb import Mydb
from estates.models import Estate
from settings_database import session, engine

import pandas as pd

TESTROWS = []
# テストに使うデータを読み込む
df = pd.read_csv("tests/csv/testdata_db.csv")
TESTROWS = df.to_dict(orient="records")
# 不要データ削除
mydb = Mydb()
mydb.engine.execute("DELETE FROM estates;")


class MydbTest(ut.TestCase):
    """Mydbのテスト"""

    def setUp(self):
        self.mydb = Mydb()
        self.engine = self.mydb.engine

    def test_init(self):
        """mydbを生成した際DBと接続されているか確認"""
        res = self.engine
        self.assertNotEqual(None, res)

    def test_delete_estate(self):
        """estate 削除"""

        # 削除成功時はTrueが返る
        id = self.mydb.insert_estate(TESTROWS[1])
        res = self.mydb.delete_estate(id)
        self.assertTrue(res)
        # 削除したデータが残っていない
        estate = session.query(Estate).filter(Estate.id == id).first()
        self.assertEqual(estate, None)

        # キーが存在しない場合はFalse が返る
        res = self.mydb.delete_estate(id)
        self.assertFalse(res)

    def test_record_count(self):
        """idを指定してレコード数を取得する"""

        row = TESTROWS[2]
        # 存在しないデータは0
        res = self.mydb.record_count("estates", "hoge")
        self.assertEqual(False, res)

        # 存在するデータはTrueが返る
        self.mydb.insert_estate(row)
        res = self.mydb.record_count("estates", row["id"])
        self.assertEqual(True, res)

    def test_insert_estate(self):
        """挿入のテスト"""

        # 一度目はTrue
        row = TESTROWS[0]
        id = row["id"]
        self.mydb.delete_estate(id)
        res = self.mydb.insert_estate(row)
        estate = session.query(Estate).filter(Estate.id == id).first()
        self.assertEqual(estate.id, res)

        # ２回目の挿入はFalse
        res = self.mydb.insert_estate(row)
        self.assertEqual(False, res)

    def test_all_estate_to_csv(self):
        """すべてのestateをCSVに保存"""
        filename = "./tmp/all_estate.csv"
        res = self.mydb.all_estate_to_csv(filename)

        self.assertEqual(filename, res)
