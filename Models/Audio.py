import base64


class Audio:
    """
    Properties:
        name
        data
        encoding
        path
    """

    def __init__(self):
        self.name = None
        self.data = None
        self.encoding = None
        self.path = None

    def __int__(self, name, data, encoding, path):
        self.name = name
        self.data = data
        self.encoding = encoding
        self.path = path

    def change_data_format_from_b64_into_b2(self):
        if self.encoding == "b64" or self.encoding is None:
            self.data = base64.b64decode(self.data)
            self.encoding = "b2"

    def change_data_format_from_b2_into_b64(self):
        if self.encoding == "b2" or self.encoding is None:
            self.data = base64.b64encode(self.data)
            self.encoding = "b64"
