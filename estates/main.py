import datetime
import requests
from bs4 import BeautifulSoup
import hashlib
import re
import pandas as pd

from pathlib import Path
import time
import os


from estates import sheet as gs
from estates.Mydb import Mydb

db = Mydb()


sumo_domain = "https://suumo.jp/"

# 取得時刻
NOWTIME = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

# 物件情報取得処理
def get_estate(get_url):
    r = requests.get(get_url)
    estates = html_to_estates(r.content)
    return estates


def html_to_estates(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    estates = soup.select("div.property_unit")
    return estates


# 都道府県と市町村を抽出
def get_prefecture_city(content):

    pattern = "(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)"

    result = re.match(pattern, content)
    prefecture = ""
    city = ""
    if result:
        prefecture = result.group(1)
        city = result.group(2)
    else:
        # 都道府県のみ
        pattern2 = "(...??[都道府県])"
        result_prefecture = re.match(pattern2, content)

        if result_prefecture:
            prefecture = result_prefecture.group(1)

    return prefecture, city


def str_to_int(s):
    """文字列を数値に変換して返す。変換できない場合は0を返す"""

    if not s.isdecimal():
        try:
            i = float(s)
        except ValueError:
            i = 0
    else:
        i = int(s)
    return i


# 物件
def estate_price(e):
    """金額取得処理"""
    price_str = e.select_one(".dottable-value").getText()
    price = estate_price_form_str(price_str)
    return price


def estate_price_form_str(price_str):
    """金額の文字列から数値としての価格を取得する（処理が複雑なので分離）"""

    # 円より後ろは無視
    if "円" in price_str:
        price_str = price_str.split("円")[0] + "円"

    price_str = price_str.replace("億円", "0000").replace("万円", "")
    # 万以下は無視
    price_str = re.sub("万.+円", "", price_str)
    # 億以上で万円が付く場合の処理
    if "億" in price_str:
        res = price_str.split("億")
        price_str = str(int(res[0]) * 10000 + int(res[1]))

    # 数値のみを抽出する
    price_str = re.sub(r"\D", "", price_str)
    price = str_to_int(price_str)

    return price


def estate_shop(e):
    """店舗情報を抽出"""
    shop = e.select_one(".shopmore-title")
    if shop:
        shop = shop.getText().replace("\t", "").replace("\n", "").replace("\r", "")
    else:
        shop = ""

    return shop


def estate_place(e):
    """ "場所と駅等を含む部分を返す"""
    # ddが１つ余計にはいっている場合の対策
    dt_name = e.select(".dottable-line > dl > dt")[2].getText()
    if dt_name == "所在地":
        place = e.select(".dottable-line > dl > dd")[2].getText()
        t = e.select(".dottable-line > dl > dd")[3].getText()
    else:
        place = e.select(".dottable-line > dl > dd")[1].getText()
        t = e.select(".dottable-line > dl > dd")[2].getText()

    return t, place


def estate_tag_route_station_work(t):
    """部分HTMLから物件の路線を取得"""
    if "「" in t and "」" in t:
        res = re.match(r"(.+)「(.+)」(.+)$", t)
        if res:
            cnt = len(res.groups())
            route = res.group(1) if cnt > 0 else ""
            station = res.group(2) if cnt > 1 else ""
            work = res.group(3) if cnt > 2 else ""
    else:
        route = ""
        station = ""
        work = ""
    return route, station, work


def estate_area_buildingarea_to_int(str):
    """土地面積と建物面積を抽出し、数値として返す"""

    if "m2" in str:
        str = str.split("m2")[0]
    if "㎡" in str:
        str = str.split("㎡")[0]
    num = str_to_int(str)
    return num


def picup_estates(estate_elems):
    """BSオブジェクトから物件情報を抽出"""
    estates = []
    i = 0
    for e in estate_elems:
        h = {}
        h["id"] = ""
        h["note"] = e.select_one(".property_unit-title").getText().replace("\n", "")

        h["price"] = estate_price(e)

        h["shop"] = estate_shop(e)

        t, h["place"] = estate_place(e)
        # 都道府県・市町村を取得
        h["prefecture"], h["city"] = get_prefecture_city(h["place"])

        # tを分割する
        route, station, work = estate_tag_route_station_work(t)
        h["station"] = station
        h["route"] = route
        h["work"] = work

        d = e.select(".dottable-line > table.dottable-fix dd")
        h["area"] = estate_area_buildingarea_to_int(d[0].getText())
        h["buildingarea"] = estate_area_buildingarea_to_int(d[2].getText())
        h["ldk"] = d[1].getText()
        h["buildingyear"] = str(d[3].getText())
        h["url"] = sumo_domain + e.select_one(".property_unit-title a")["href"]

        h["created"] = NOWTIME

        # ハッシュ値の生成
        txt = str(h["price"]) + h["place"] + str(h["area"]) + str(h["buildingarea"])
        h["id"] = create_hash(txt)

        estates.append(h)

    return estates


# ハッシュ値の生成
def create_hash(txt):
    hash = hashlib.sha256(txt.encode("utf-8")).hexdigest()
    return hash


# pandasでCSV変換
def to_csv(estates, filename):
    df = pd.DataFrame(data=estates)
    df.to_csv(filename, index=False)


def create_time_check(filename):
    """CSV取得から１時間経過していなかったらFalse"""

    # ファイルが存在しない場合はTrue
    if os.path.isfile(filename) == False:
        return True

    p = Path(filename)
    create_time = p.stat().st_ctime
    now = time.time()

    # 3600秒 3時間以上立っている場合はTrue
    after_time = now - (create_time + (3600 * 3))

    if after_time > 0:
        return True
    else:
        return False


def insert_estate_csv(csv_filename):
    """取得したCSVをDBに登録 登録した件数を返す"""

    # CSVファイルにデータがない場合対策
    try:
        df = pd.read_csv(csv_filename)
    except Exception as e:
        return 0

    rows = df.to_dict(orient="records")

    cnt = 0
    for row in rows:
        res = db.insert_estate_new_data(row)
        if res:
            print(row["price"], row["note"])
            cnt += 1

    return cnt


def update_sheet(csv_filename, sheetname):
    """postgresqlの最新データでsheetの内容を書き換える"""

    db.all_estate_to_csv(csv_filename)
    gs.set_csv_to_sheet(csv_filename, sheetname)


def web_to_csv_and_db(get_url, csv_filename):
    # 速度対策で、処理が５時間以内にされている場合は、CSV取得処理をスキップして処理続行
    if create_time_check(csv_filename):
        # 処理前に3秒間隔をあける
        time.sleep(3)
        estates = picup_estates(get_estate(get_url))
        to_csv(estates, csv_filename)

        result = insert_estate_csv(csv_filename)

    else:
        result = "SKIP"

    return result
