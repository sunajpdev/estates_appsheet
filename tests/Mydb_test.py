import unittest as ut
from estates.mydb import Mydb
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

    def test_init_db(self):
        """テーブルが作成される"""
        self.mydb.init_db()
        res = self.mydb.insert_estate(TESTROWS[3])

        self.assertTrue(res)

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

        # 失敗しているケース
        row = {
            "id": "48e077ba80be0a9fa1760d8c4feeba4e7b027552c8dec6a17bf991d9e61393f4",
            "note": "成育３（野江駅） 3480万円",
            "price": "3480",
            "shop": "(株)福屋不動産販売京橋店",
            "place": "大阪府大阪市城東区成育３",
            "prefecture": "大阪府",
            "city": "大阪市城東区",
            "station": "野江",
            "route": "京阪本線",
            "work": "徒歩3分",
            "area": "75.29",
            "buildingarea": "108.31",
            "buildingyear": "2005年8月",
            "ldk": "4LDK",
            "url": "https://suumo.jp//chukoikkodate/osaka/sc_osakashijoto/nc_96055204/",
            "created": "2021/6/15",
        }
        id = row["id"]
        self.mydb.delete_estate(id)
        res = self.mydb.insert_estate(row)
        estate = session.query(Estate).filter(Estate.id == id).first()
        self.assertEqual(estate.id, res)

        row = {
            "id": "858fe6ff8e43934764a382a994c75f584f00606301a91dd6ca872de6d53f85d5",
            "note": "◆京王線で新宿方向へ、JR南武線で川崎・横浜方向へ\u30002路線利用可能な通勤・…",
            "price": 1800,
            "shop": "アルカス住宅販売(株)",
            "place": "神奈川県川崎市多摩区菅馬場２",
            "prefecture": "神奈川県",
            "city": "川崎市多摩区",
            "station": "稲田堤",
            "route": "ＪＲ南武線",
            "work": "徒歩13分",
            "area": 49.64,
            "buildingarea": 72.09,
            "buildingyear": "1991年9月",
            "ldk": "4LDK",
            "url": "https://suumo.jp//chukoikkodate/kanagawa/sc_kawasakishitama/nc_95659875/",
            "created": "2021/6/10",
        }
        id = row["id"]
        self.mydb.delete_estate(id)
        res = self.mydb.insert_estate(row)
        estate = session.query(Estate).filter(Estate.id == id).first()
        self.assertEqual(estate.id, res)

    def test_all_estate_to_csv(self):
        """すべてのestateをCSVに保存"""
        filename = "./tmp/all_estate.csv"
        res = self.mydb.all_estate_to_csv(filename)

        self.assertEqual(filename, res)
