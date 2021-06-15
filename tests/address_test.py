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
        self.assertEqual("", prefecture)
        self.assertEqual("", city)
