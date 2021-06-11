import configparser


class MyConfig:
    """ 設定ファイルの読み込みを管理する """

    def __init__(self):
        """ 環境設定を読み込み開発環境か本番環境かで読み込む設定ファイルを変更する """

        self.ini = configparser.ConfigParser()
        self.ini.read("config.ini", encoding="utf-8")

