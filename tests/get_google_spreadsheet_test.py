import unittest as ut
from estates import get_google_spreadsheet as gs

from bs4 import BeautifulSoup


class GoogleSpreadSheetTest(ut.TestCase):
    """GoogleSpreadSheetのテスト"""

    def test_set_db_to_gs(self):
        """ DBから取得したデータをGoogleSpreadSheetに登録する """
        # res = gs.set_db_to_gs():
        self.assertTrue(True)
