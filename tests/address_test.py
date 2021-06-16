import unittest as ut
from mylib.address import Address


class AddressTest(ut.TestCase):
    """Addressのテスト"""

    def test_address_to_prefecture_and_city(self):
        """住所から都道府県・市町村が正常に取得できるか確認"""

        # 東京都
        address = "東京都八王子市下柚木３"
        prefecture, city = Address.address_to_prefecture_and_city(address)
        self.assertEqual("東京都", prefecture)
        self.assertEqual("八王子市", city)

        # 都道府県のみ
        address = "大阪府"
        prefecture, city = Address.address_to_prefecture_and_city(address)
        self.assertEqual("大阪府", prefecture)
        self.assertEqual("", city)

        # 無効な住所
        address = "ほげほげ大阪"
        prefecture, city = Address.address_to_prefecture_and_city(address)
        self.assertEqual("", prefecture)
        self.assertEqual("", city)

        # 無効な住所
        address = "ほげほげ東京都八王子市下柚木３"
        prefecture, city = Address.address_to_prefecture_and_city(address)
        self.assertEqual("東京都", prefecture)
        self.assertEqual("八王子市", city)

        # 日本、〒292-0051 千葉県木更津市清川１丁目１９−２  2021/6/15
        address = "日本、〒292-0051 千葉県木更津市清川１丁目１９−２"
        prefecture, city = Address.address_to_prefecture_and_city(address)
        self.assertEqual("千葉県", prefecture)
        self.assertEqual("木更津市", city)

        # 北海道
        address = "〒060-0808 北海道札幌市北区北８条西５丁目"
        prefecture, city = Address.address_to_prefecture_and_city(address)
        self.assertEqual("北海道", prefecture)
        self.assertEqual("札幌市北区", city)

        # 京都府
        address = "〒606-8501 京都府京都市左京区吉田本町"
        prefecture, city = Address.address_to_prefecture_and_city(address)
        self.assertEqual("京都府", prefecture)
        self.assertEqual("京都市左京区", city)

        # 神奈川県
        address = "〒221-8686 神奈川県横浜市神奈川区六角橋３丁目２７−１"
        prefecture, city = Address.address_to_prefecture_and_city(address)
        self.assertEqual("神奈川県", prefecture)
        self.assertEqual("横浜市神奈川区", city)

    def test_address_to_prefecture(self):

        # 前に余計な文字がある
        address = "日本、〒292-0051 千葉県木更津市清川１丁目１９−２"
        res = Address.address_to_prefecture(address)
        self.assertEqual("千葉県", res)

        # 前に余計な文字がある
        address = "ほげほげ東京都八王子市下柚木３"
        res = Address.address_to_prefecture(address)
        self.assertEqual("東京都", res)

        # 無効な住所
        address = "ほげほげ大阪"
        res = Address.address_to_prefecture(address)
        self.assertEqual("", res)

        # 東京都
        address = "東京都八王子市下柚木３"
        res = Address.address_to_prefecture(address)
        self.assertEqual("東京都", res)

    def test_address_orthopaedy(self):

        # 前に余計な文字がある
        address = "日本、〒292-0051 千葉県木更津市清川１丁目１９−２"
        res = Address.address_orthopaedy(address)
        self.assertEqual("千葉県木更津市清川１丁目１９−２", res)

        # 前に余計な文字がある
        address = "ほげほげ東京都八王子市下柚木３"
        res = Address.address_orthopaedy(address)
        self.assertEqual("東京都八王子市下柚木３", res)

        # 無効な住所
        address = "ほげほげ大阪"
        res = Address.address_orthopaedy(address)
        self.assertEqual("ほげほげ大阪", res)

        # 東京都
        address = "東京都八王子市下柚木３"
        res = Address.address_orthopaedy(address)
        self.assertEqual("東京都八王子市下柚木３", res)
