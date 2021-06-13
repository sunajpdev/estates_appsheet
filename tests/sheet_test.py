import unittest as ut
from estates import sheet as gs

from bs4 import BeautifulSoup


class GoogleSpreadSheetTest(ut.TestCase):
    """GoogleSpreadSheetのテスト"""

    def test_set_csv_to_sheet(self):
        """DBから取得したデータをGoogleSpreadSheetに登録する"""

        #  ファイルがある場合はTrue
        csv_filename = "tests/csv/test_data01.csv"
        sheetname = "test"
        res = gs.set_csv_to_sheet(csv_filename, sheetname)
        self.assertTrue(res)

        # ファイルがない場合はFalse
        csv_filename = "tests/csv/test_notfile.csv"
        sheetname = "test"
        res = gs.set_csv_to_sheet(csv_filename, sheetname)
        self.assertFalse(res)
