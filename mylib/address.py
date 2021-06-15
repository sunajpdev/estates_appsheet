import re


class Address:
    @classmethod
    def address_to_prefecture_and_city(cls, address):
        """住所から都道府県と市町村を抽出
        戻り値: 都道府県、市町村
        """

        pattern = "(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)"

        result = re.match(pattern, address)
        prefecture = ""
        city = ""
        if result:
            prefecture = result.group(1)
            city = result.group(2)
        else:
            # 都道府県のみ
            pattern2 = "(...??[都道府県])"
            result_prefecture = re.match(pattern2, address)

            if result_prefecture:
                prefecture = result_prefecture.group(1)

        return prefecture, city
