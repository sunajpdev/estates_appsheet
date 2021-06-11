import gspread
import json
import time
import pandas as pd

# 環境設定読み込み
# import configparser

# ini = configparser.ConfigParser()
# ini.read("config.ini", encoding="utf-8")


from mylib import MyConfig as cf

# Googleスプレッドシート関係の設定
# ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
# keyfile = "python-web-getter-4f9bb7bee43d.json"
keyfile = cf.ini.get("GSHEET", "keyfile")

# 認証情報設定
credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)

# OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

# 処理をするスプレッドシートの名称
SHEET_NAME = cf.ini.get("GSHEET", "sheetname")

# 比較対象として一時ダウンロードするグーグルスプレッドシート
CSVFILENAME = "tmp/_gs.csv"

# 共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = cf.ini.get("GSHEET", "spreadsheet_key")

# 共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

# GoogleSpreadSheetsから取り込む
def download_as_df(sheet_id, sheet_name):
    from df2gspread import gspread2df as g2d

    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)
    df = g2d.download(
        sheet_id,
        wks_name=sheet_name,
        col_names=True,
        row_names=False,
        credentials=credentials,
        start_cell="A1",
    )
    return df


# GoogleスプレッドシートをCSVとしてダウンロードする
def get_google_spread_rows():
    df = download_as_df(SPREADSHEET_KEY, SHEET_NAME)
    df.to_csv(CSVFILENAME, index=False)


## CSVファイルに指定したCSVを結合して保存する
def append_estate_csv(filename1, filename2):
    """ ダウンロードしたCSVに今回処理したestateを含むCSVを追加する（ハッシュダブリ防止） """
    df1 = pd.read_csv(filename1)
    df2 = pd.read_csv(filename2)


# 取得したCSVから新規データのみをGoogleスプレッドシートに登録する
def append_new_estate(csv_filename):
    df1 = pd.read_csv(CSVFILENAME)
    df2 = pd.read_csv(csv_filename)

    # 差分取得
    ids = ids = df1["id"]
    df_diff = df2[~df2["id"].isin(ids)]

    # pandasデータをリストに変換 欠損値は空白にする
    diff_list = df_diff.fillna("").values.tolist()

    # シートへ書き込み
    # 10回書き込んだら10秒待機
    i = 0
    add_hash_list = []
    for row in diff_list:
        id = row[0]
        if id not in add_hash_list:
            i = i + 1
            print("[ADD]", row)
            worksheet.append_row(row)
            add_hash_list.append(id)
        else:
            print("[SKIP]", row)

        # GoogleAPIの制約により１０件書き込む毎に10秒スリープ　これ以下だとエラーになる
        if i > 10:
            time.sleep(10)
            i = 0

    # ダウンロードしたCSVを結合して保存
    df = pd.concat([df1, df2])
    df.to_csv(CSVFILENAME, index=False)

    return df_diff
