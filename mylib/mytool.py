import json


class MyTool:
    @classmethod
    def json_file_to_dict(cls, filename):
        """jsonを読み込んでdictとして返す"""

        with open(filename, "r") as f:
            jsn = json.load(f)

        return jsn
