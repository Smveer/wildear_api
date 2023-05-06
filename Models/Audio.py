import base64


class Audio:
    """
    Properties:
        name
        data
        encoding
        path
    """

    def __init__(self, json_dic=None):
        if json_dic:
            if json_dic["data"]:
                self.set_data(base64.b64decode(json_dic["data"]))
            if json_dic["name"]:
                self.set_name(json_dic["name"])
            if json_dic["path"]:
                self.set_path(json_dic["path"])
            self.change_data_format_from_b64_into_b2()
        else:
            self.name = None
            self.data = None
            self.encoding = None
            self.path = None

    def set_data(self, data):
        self.data = data

    def set_name(self, name):
        self.name = name

    def set_path(self, path):
        self.path = path

    def set_encoding(self, encoding):
        self.encoding = encoding

    def change_data_format_from_b64_into_b2(self):
        if self.encoding == "b64" or self.encoding is None:
            self.set_data(base64.b64decode(self.data))
            self.set_encoding("b2")

    def change_data_format_from_b2_into_b64(self):
        if self.encoding == "b2" or self.encoding is None:
            self.set_data(base64.b64encode(self.data))
            self.set_encoding("b64")
