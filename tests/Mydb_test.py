import unittest as ut
from mylib.Mydb import Mydb


class MydbTest(ut.TestCase):
    """Mydbのテスト"""

    estate1 = {
        "id": "test",
        "note": "note",
        "price": 1000,
        "shop": "test",
        "shop": "",
        "place": "",
        "prefecture": "",
        "city": "",
        "station": "",
        "route": "",
        "work": "",
        "area": 0,
        "buildingarea": 0,
        "ldk": "",
        "buildingyear": "",
        "url": "",
    }

    def setUpModule(self):
        # estatesを削除する
        mydb = Mydb()
        mydb.engine.execute("DELETE FROM estates;")

    def setUp(self):
        self.mydb = Mydb()
        self.engine = self.mydb.engine

    def test_init(self):
        """ mydbを生成した際DBと接続されているか確認 """
        res = self.engine
        self.assertNotEqual(None, res)

    def test_delete_estate(self):
        """ estate 削除 """

        estate_del = {
            "id": "del",
            "note": "note",
            "price": 1000,
            "shop": "test",
            "shop": "",
            "place": "",
            "prefecture": "",
            "city": "",
            "station": "",
            "route": "",
            "work": "",
            "area": 0,
            "buildingarea": 0,
            "ldk": "",
            "buildingyear": "",
            "url": "",
        }

        id = self.mydb.insert_estate(estate_del)
        res = self.mydb.delete_estate(id)
        self.assertTrue(res)

        # キーが存在しない場合もエラーにならない
        res = self.mydb.delete_estate(id)
        self.assertTrue(res)

    def test_record_count(self):
        """ idを指定してレコード数を取得する """

        # 存在しないデータは0
        row = self.mydb.record_count("estates", "hoge")
        self.assertEqual(0, row)

        # 存在するデータはレコード数を返す
        self.mydb.insert_estate(self.estate1)
        row = self.mydb.record_count("estates", "test")
        self.assertEqual(1, row)

    def test_insert_estate(self):
        """ 挿入のテスト """

        # 一度目はTrue
        id = self.estate1["id"]
        ## 事前に削除
        self.mydb.delete_estate(id)
        res = self.mydb.insert_estate(self.estate1)
        self.assertEqual(id, res)
        # ２回目の挿入はFalse
        res = self.mydb.insert_estate(self.estate1)
        self.assertEqual(False, res)

    def test_insert_estate_new_data(self):
        """ 新規レコードが重複したケースと重複していないケース """

        id = self.estate1["id"]
        self.mydb.delete_estate(id)

        # 初回はidが返る
        res = self.mydb.insert_estate_new_data(self.estate1)
        self.assertEqual(id, res)

        # 重複の場合はFalseが返る
        res = self.mydb.insert_estate_new_data(self.estate1)
        self.assertEqual(False, res)

    def test_all_estate_to_csv(self):
        """ すべてのestateをCSVに保存 """

        filename = "./tmp/all_estate.csv"
        res = self.mydb.all_estate_to_csv(filename)

        self.assertEqual(filename, res)

