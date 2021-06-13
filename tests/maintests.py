""" メイン処理のテスト """
import unittest as ut
from estates import main
from mylib.Mydb import Mydb

from bs4 import BeautifulSoup


class MainTest(ut.TestCase):
    """Mainのテスト"""

    def setUpModule(self):
        # estatesを削除する
        mydb = Mydb()
        mydb.engine.execute("DELETE FROM estates;")

    def test_get_estate(self):
        """ 不動産情報を取得する """

        url_yokosuka = "https://suumo.jp/jj/bukken/ichiran/JJ012FC001/?ar=030&bs=021&sc=14201&ta=14&po=1&pj=2&pc=100"
        estate_elems = main.get_estate(url_yokosuka)
        self.assertNotEqual(estate_elems, False)

    def test_create_hash(self):
        """ ハッシュの生成を確認 """

        txt = ""
        hash = main.create_hash(txt)
        self.assertEqual(
            hash, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )

        txt = "29800hogehoge"
        hash = main.create_hash(txt)
        self.assertEqual(
            hash, "73553c150387ac0b5bc61b6ede3f64b55c71ad5ae294f72cf735bcc037439e4d"
        )

    def test_estate_tag_route_station_work(self):
        """ 駅などの情報から、駅名、路線名、所要時間を抽出 """

        t = "妙高はねうまライン「高田」徒歩32分"
        route, station, work = main.estate_tag_route_station_work(t)

        self.assertEqual(route, "妙高はねうまライン")
        self.assertEqual(station, "高田")
        self.assertEqual(work, "徒歩32分")

        t = ""
        route, station, work = main.estate_tag_route_station_work(t)

        self.assertEqual(route, "")
        self.assertEqual(station, "")
        self.assertEqual(work, "")

        t = "-"
        route, station, work = main.estate_tag_route_station_work(t)

        self.assertEqual(route, "")
        self.assertEqual(station, "")
        self.assertEqual(work, "")

        # 閉じカッコがないケース
        t = "ほげほえ「あああああ"
        route, station, work = main.estate_tag_route_station_work(t)

        self.assertEqual(route, "")
        self.assertEqual(station, "")
        self.assertEqual(work, "")

        # エラーになったケース　カッコ２つ
        t = "富士急静岡バス「「高山団地入口」停より徒歩」徒歩4分"
        route, station, work = main.estate_tag_route_station_work(t)

        self.assertEqual(route, "富士急静岡バス「")
        self.assertEqual(station, "高山団地入口」停より徒歩")
        self.assertEqual(work, "徒歩4分")

    def test_estate_price(self):
        """ 価格取得処理のテスト """
        filename = "tests/html/estates.html"
        estates = main.html_to_estates(open(filename))
        # 通常ケース
        e = estates[0]
        price = main.estate_price(e)
        self.assertEqual(price, 2390)

        # 文字列があるケース 文字列：　2580※権利金含む
        e = estates[1]
        price = main.estate_price(e)
        self.assertEqual(price, 2580)

    def test_estate_price_form_str(self):
        """ いろいろな価格文字列のケースを想定 """

        s = ""
        price = main.estate_price_form_str(s)
        self.assertEqual(price, 0)

        s = "2356"
        price = main.estate_price_form_str(s)
        self.assertEqual(price, 2356)

        # 円の場合は間違いと想定して、万円と同様の処理
        s = "2356円"
        price = main.estate_price_form_str(s)
        self.assertEqual(price, 2356)

        s = "2356万円"
        price = main.estate_price_form_str(s)
        self.assertEqual(price, 2356)

        s = "2,356万円"
        price = main.estate_price_form_str(s)
        self.assertEqual(price, 2356)

        s = "99億円"
        price = main.estate_price_form_str(s)
        self.assertEqual(price, 990000)

        s = "99億2356万円"
        price = main.estate_price_form_str(s)
        self.assertEqual(price, 992356)

        s = "ある2,356円"
        price = main.estate_price_form_str(s)
        self.assertEqual(price, 2356)

        s = "ある2,356円～"
        price = main.estate_price_form_str(s)
        self.assertEqual(price, 2356)

        s = "ある2,356円～2500円"
        price = main.estate_price_form_str(s)
        self.assertEqual(price, 2356)

    def test_estate_area_buildingarea_to_int(self):
        """ 面積を含む数字文字列から面積を数値で取得する """

        s = "455.71m2（137.85坪）（登記）"
        i = main.estate_area_buildingarea_to_int(s)
        self.assertEqual(i, 455.71)

        # m2が存在しない場合
        s = "455.71m（137.85坪）（登記）"
        i = main.estate_area_buildingarea_to_int(s)
        self.assertEqual(i, 0)

    def test_picup_estates(self):
        """ 取得したHTMLから不動産情報を抽出 全体的なテストなので一番下"""

        filename = "tests/html/yokosuka.html"
        soup = main.html_to_estates(open(filename))
        estates = main.picup_estates(soup)

        self.assertEqual(
            estates[0]["id"],
            "ed09d1eb22360c8066feab3ed90555488d26b8e042e652602bf60d928f462a86",
        )

        self.assertEqual(estates[0]["price"], 1040)
        self.assertEqual(estates[0]["place"], "神奈川県横須賀市小矢部１")
        self.assertEqual(estates[0]["prefecture"], "神奈川県")
        self.assertEqual(estates[0]["city"], "横須賀市")
        self.assertEqual(estates[0]["station"], "衣笠")
        self.assertEqual(estates[0]["route"], "ＪＲ横須賀線")
        self.assertEqual(estates[0]["area"], 455.71)
        self.assertEqual(estates[0]["buildingarea"], 61.48)

        # 2021/5/18 上越エラー
        filename = "tests/html/jouetu.html"
        soup = main.html_to_estates(open(filename))
        estates = main.picup_estates(soup)

        self.assertEqual(
            estates[0]["id"],
            "e93510230944e66657881e5f7ead6c4b2f7852647da35e6678f1dc1b5d412cab",
        )
        self.assertEqual(estates[0]["price"], 150)
        self.assertEqual(estates[0]["place"], "新潟県上越市大字戸野目856")
        self.assertEqual(estates[0]["prefecture"], "新潟県")
        self.assertEqual(estates[0]["city"], "上越市")
        self.assertEqual(estates[0]["station"], "高田")
        self.assertEqual(estates[0]["route"], "妙高はねうまライン")
        self.assertEqual(estates[0]["area"], 386.86)
        self.assertEqual(estates[0]["buildingarea"], 175.69)

    def test_insert_estate_to_csv(self):
        """ CSVからDBに登録する """

        # データがある場合
        csv_filename = "tests/csv/test_data01.csv"
        res = main.insert_estate_csv(csv_filename)
        self.assertEqual(0, res)

        # データがない場合
        csv_filename = "tests/csv/test_nodata.csv"
        res = main.insert_estate_csv(csv_filename)
        self.assertEqual(0, res)


