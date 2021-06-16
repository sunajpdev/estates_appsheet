import sys
import pathlib
from typing import Dict

# base.pyのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append(str(current_dir) + "/../")


import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

from mylib.mypandas import MyPandas as mp


def main(url, prefecture, prefecture_name):

    res = requests.get(url)

    soup = bs(res.content, "html.parser")

    cities = soup.select(".itemlinebox  ul.itemtoplist li a")

    list_url = []
    for c in cities:
        url = "https://suumo.jp" + c.get("href")
        city_name = c.get_text()
        print(city_name)
        try:
            res2 = requests.get(url)
            soup2 = bs(res2.content, "html.parser")
            link = soup2.select("div.sortbox > dl > dd > a")[1].get("href")
            link = "https://suumo.jp" + link.replace("&pc=30", "&pc=100&po=1&pj=2")
            list_url.append(
                {
                    "prefecture": prefecture,
                    "prefecture_name": prefecture_name,
                    "city_name": city_name,
                    "url": link,
                }
            )
        except:
            pass
    return list_url


def get_all_prefectures_url():
    """SUMOの全国の市町村のURLを取得してCSVとして保存する"""
    prefectures = {
        "hokkaido_": "北海道",
        "aomori": "青森県",
        "akita": "秋田県",
        "iwate": "岩手県",
        "miyagi": "宮城県",
        "yamagata": "山形県",
        "fukushima": "福島県",
        "ibaraki": "茨城県",
        "gumma": "群馬県",
        "tochigi": "栃木県",
        "chiba": "千葉県",
        "saitama": "埼玉県",
        "kanagawa": "神奈川県",
        "tokyo": "東京都",
        "niigata": "新潟県",
        "nagano": "長野県",
        "yamanashi": "山梨県",
        "toyama": "富山県",
        "ishikawa": "石川県",
        "fukui": "福井県",
        "shizuoka": "静岡県",
        "aichi": "愛知県",
        "mie": "三重県",
        "gifu": "岐阜県",
        "wakayama": "和歌山県",
        "nara": "奈良県",
        "siga": "滋賀県",
        "kyoto": "京都府",
        "hyogo": "兵庫県",
        "osaka": "大阪府",
        "hiroshima": "広島県",
        "okayama": "岡山県",
        "tottori": "鳥取県",
        "shimane": "島根県",
        "yamaguchi": "山口県",
        "kagawa": "香川県",
        "tokushima": "徳島県",
        "ehime": "愛媛県",
        "kouchi": "高知県",
        "fukuoka": "福岡県",
        "saga": "佐賀県",
        "nagasaki": "長崎県",
        "kumamoto": "熊本県",
        "oita": "大分県",
        "miyazaki": "宮崎県",
        "kagoshima": "鹿児島県",
        "okinawa": "沖縄県",
    }

    return prefectures


if __name__ == "__main__":

    print("### start main ###")

    prefectures = get_all_prefectures_url()
    urls = []
    for prefecture, prefecture_name in prefectures.items():
        url = f"https://suumo.jp/chukoikkodate/{prefecture}/"
        res = main(url, prefecture, prefecture_name)
        urls.extend(res)
    df = pd.DataFrame(data=urls)
    df.to_csv("data/cities_url.csv", index=False)

    print("### end start ###")
