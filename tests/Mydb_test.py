import unittest as ut
from mylib import Mydb


class MydbTest(ut.TestCase):
    """Mydbのテスト"""

    def test_init(self):
        """ mydbを生成する """
        mydb = Mydb.Mydb()
        res = mydb.engine.execute("SELECT * FROM estates limit 10")

        self.assertEqual("hoge", res)

    def test_return_true(self):
        mydb = Mydb.Mydb()
        res = mydb.return_true
        self.assertTrue(res)

