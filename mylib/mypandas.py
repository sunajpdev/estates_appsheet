import pandas as pd


class MyPandas:
    """pandasでよく使う処理をまとめるためのクラス"""

    @classmethod
    def to_csv(cls, arr_dict, filename):
        """辞書からCSV変換"""

        try:
            df = pd.DataFrame(data=arr_dict)
            df.to_csv(filename, index=False)
            return True
        except FileNotFoundError:
            return False
        except ValueError:
            return False

    @classmethod
    def read_arr_dict(cls, arr_dict):
        """辞書をデータソースとして読み込む"""

        df = pd.DataFrame(data=arr_dict)

        return df
