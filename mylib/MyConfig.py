import configparser


class MyConfig:
    """ 設定ファイルの読み込みを管理する """

    def __init__(self):
        """ 環境設定を読み込み開発環境か本番環境かで読み込む設定ファイルを変更する """

        env = configparser.ConfigParser()
        env.read(".env", encoding="utf-8")

        # 開発環境と本番環境で別々のconfig.iniを読み込む
        self.ini = configparser.ConfigParser()
        if env["Default"]["mode"] == "Production":
            config_filename = env["Production"]["config_filename"]
        else:
            config_filename = env["Development"]["config_filename"]

        self.ini.read(config_filename, encoding="utf-8")

