import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from settings import ReadIni

cf = ReadIni()


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

# 共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = cf.ini.get("GSHEET", "spreadsheet_key")


def set_csv_to_sheet(csv_path, sheet_name):
    """CSVデータによりシートを一括で書き換える"""
    import csv

    workbook = gc.open_by_key(SPREADSHEET_KEY)
    result = True
    try:
        workbook.values_update(
            sheet_name,
            params={"valueInputOption": "USER_ENTERED"},
            body={"values": list(csv.reader(open(csv_path)))},
        )
    except Exception as e:
        print("### ERROR ###", e)
        result = False

    return result
