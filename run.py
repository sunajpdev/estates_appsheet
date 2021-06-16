import pandas as pd

from estates import main
import settings_city


csv_filename = "data/cities_url.csv"
df = pd.read_csv(csv_filename)
rows = df.to_dict(orient="records")
for row in rows:
    csv_filename = "./tmp/" + row["prefecture_name"] + row["city_name"] + ".csv"
    url = row["url"]
    print("###", row["prefecture_name"], row["city_name"])
    res = main.web_to_csv_and_db(url, csv_filename)
    print("Insert: ", res)

# GoogleSpreadSheet更新処理
print("### Sheet update start ###")
csv_filename = "tmp/upload.csv"
sheetname = "estates"
main.update_sheet(csv_filename, sheetname)
print("### Sheet update end ###")
