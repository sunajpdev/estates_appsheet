import unittest as ut
from mylib.mypandas import MyPandas as mp

import os


class MyPandasTest(ut.TestCase):
    """MyPandasのテスト"""

    def test_to_csv(self):
        """辞書からCSVを作成する"""

        dict = [{"id": "test", "name": "hogehoge", "age": 10}]
        filename = "tests/tmp/mypandas_to_csv_test.csv"
        res = mp.to_csv(dict, filename)
        self.assertTrue(res)
        exists = os.path.isfile(filename)
        self.assertTrue(exists)

        # 複数行
        dict = [
            {"id": "test1", "name": "hogehoge1", "age": 10},
            {"id": "test2", "name": "hogehoge2", "age": 20},
            {"id": "test3", "name": "hogehoge3", "age": 30},
        ]
        filename = "tests/tmp/mypandas_to_csv_test02.csv"
        res = mp.to_csv(dict, filename)
        self.assertTrue(res)
        exists = os.path.isfile(filename)
        self.assertTrue(exists)

        # 項目がない項目がある場合も正常に作成される
        dict = [
            {"id": "test1", "name": "hogehoge1", "age": 10},
            {"id": "test2", "name": "hogehoge2", "age": 20, "address": "japan tokyo"},
        ]
        filename = "tests/tmp/mypandas_to_csv_test03.csv"
        res = mp.to_csv(dict, filename)
        self.assertTrue(res)
        exists = os.path.isfile(filename)
        self.assertTrue(exists)

        # ディレクトリが存在せずｃｓｖファイルが作成できない場合はFalseを返す
        dict = [
            {"id": "test1", "name": "hogehoge1", "age": 10},
            {"id": "test2", "name": "hogehoge2", "age": 20, "address": "japan tokyo"},
        ]
        filename = "tests/tmp/tmp/mypandas_to_csv_test04.csv"
        res = mp.to_csv(dict, filename)
        self.assertFalse(res)
        exists = os.path.isfile(filename)
        self.assertFalse(exists)

        # arr_dictが空の場合はFalseを返す
        dict = []
        filename = "tests/tmp/tmp/mypandas_to_csv_test04.csv"
        res = mp.to_csv(dict, filename)
        self.assertFalse(res)
        exists = os.path.isfile(filename)
        self.assertFalse(exists)

        # arr_dictが文字列の場合はFalseを返す
        dict = ""
        filename = "tests/tmp/tmp/mypandas_to_csv_test04.csv"
        res = mp.to_csv(dict, filename)
        self.assertFalse(res)
        exists = os.path.isfile(filename)
        self.assertFalse(exists)

        # arr_dictが数字の場合はFalseを返す
        dict = 19
        filename = "tests/tmp/tmp/mypandas_to_csv_test04.csv"
        res = mp.to_csv(dict, filename)
        self.assertFalse(res)
        exists = os.path.isfile(filename)
        self.assertFalse(exists)

        # arr_dictが辞書の場合はFalseを返す
        dict = {"id": "test1", "name": "hogehoge1", "age": 10}
        filename = "tests/tmp/tmp/mypandas_to_csv_test04.csv"
        res = mp.to_csv(dict, filename)
        self.assertFalse(res)
        exists = os.path.isfile(filename)
        self.assertFalse(exists)
