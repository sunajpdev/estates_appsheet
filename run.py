from estates import main
from estates import get_google_spreadsheet

import settings_city

cities = settings_city.cities


for prefecture in cities:
    for city, url in prefecture.items():
        print("###", city)
        csv_filename = f"./tmp/_{city}.csv"
        res = main.web_to_csv_and_db(url, csv_filename)
        print("Insert: ", res)
# GoogleSpreadSheet更新処理
print("### Sheet update start ###")
csv_filename = "tmp/upload.csv"
sheetname = "estates"
main.update_sheet(csv_filename, sheetname)
print("### Sheet update end ###")
