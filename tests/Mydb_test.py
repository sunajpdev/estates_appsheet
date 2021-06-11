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

    def setUp(self):
        print("setup")
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

    def test_insert_estate(self):
        """ 挿入のテスト """

        # 一度目はTrue
        id = self.estate1["id"]
        res = self.mydb.insert_estate(self.estate1)
        self.assertEqual(id, res)
        # キーが重複した場合はTrue以外
        res = self.mydb.insert_estate(self.estate1)
        self.assertNotEqual(True, res)

