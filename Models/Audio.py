import base64


class Audio:
    """
        The class Audio represents some tools to module audio sounds
    """

    def __init__(
            self,
            json_dic: dict = None
    ):
        """
        Constructors of class Audio.

            Parameters with 1st version:
                        No parameter: init only audio

            Parameters with 2nd version:
                        json_dic (dict): json dictionary containing keys ["data"]
        """
        self.data = None
        self.encoding = None
        self.path = None
        if json_dic:
            if "data" in json_dic:
                self.set_data(json_dic["data"])
            self.change_data_format_from_b64_into_b2()

    def __eq__(
            self,
            other: 'Audio'
    ) -> bool:
        """
        Check if an instance of Audio is equal to another instance of Audio : \n
        aud, other = Audio() -> aud == other => True

            Parameters:
                    other (Audio): the other instant of Audio that you want to verify

            Returns:
                    bool
        """
        if self.path == other.path and self.data == other.data and self.encoding == other.encoding:
            return True
        return False

    def set_data(
            self,
            data: bytes
    ):
        """
        Set data into Audio instance

            Parameters:
                        data (bytes): data string formated in bytes
        """
        self.data = data

    def set_path(
            self,
            path: str
    ):
        """
        Set path into Audio instance

            Parameters:
                        path (str): path string (absolute recommended)
        """
        self.path = path

    def set_encoding(
            self,
            encoding: str
    ):
        """
        Set encoding into Audio instance

            Parameters:
                        encoding (str): "b64" or "b2"
        """
        self.encoding = encoding

    def change_data_format_from_b64_into_b2(
            self
    ):
        """
        Change data format that is Audio instance data field along with the encoding:
            "b64" to "b2"
        """
        if self.encoding == "b64" or self.encoding is None:
            self.set_data(base64.b64decode(self.data))
            self.set_encoding("b2")

    def change_data_format_from_b2_into_b64(
            self
    ):
        """
        Change data format that is Audio instance data field along with the encoding:
            "b2" to "b64"
        """
        if self.encoding == "b2" or self.encoding is None:
            self.set_data(base64.b64encode(self.data))
            self.set_encoding("b64")

    @staticmethod
    def get_filename_from_path(
            path: str,
            extension: bool = True
    ) -> str:
        """
        Static Method
        Read path string and return the filename of the file pointed:

            Parameters:
                        path (str): path of the filename to get
                        extension (bool): True as default, give the name with (True) or without (False) extension
            Returns:
                    filename (str)
        """
        if extension:
            return path.split("/")[-1]
        else:
            return path.split("/")[-1].split(".")[0]

    @staticmethod
    def get_directory_path_from_path(
            path: str,
            last_slash: bool = True
    ) -> str:
        """
        Static Method
        Read path string and return the path of directory of the file pointed:

            Parameters:
                        path (str): path of the directory to get
                        last_slash (bool): True as default , If true, retrieve last slash, else not
            Returns:
                    path (str)
        """
        if last_slash:
            return "/".join(path.split("/")[:-1]) + "/"
        return "/".join(path.split("/")[:-1])

    @staticmethod
    def get_file_extension_from_path(
            path: str,
            point: bool = True
    ) -> str:
        """
        Static Method
        Read path string and return the extension of the file pointed, uses Audio.get_filename_from_path():

            Parameters:
                        path (str): path of the filename to get its extension
                        point (bool): True as default, if True, retrieve point in front of the extension
            Returns:
                    extension (str)
        """
        if point:
            return "." + Audio.get_filename_from_path(path).split(".")[-1]
        return Audio.get_filename_from_path(path).split(".")[-1]

    @staticmethod
    def get_path_without_extension_from_path(
            path: str
    ) -> str:
        """
        Static Method
        Read path string and return the path without the extension at the end,\n
        uses Audio.get_directory_path_from_path and Audio.get_filename_from_path :

            Parameters:
                        path (str): path of the filename to get its extension
            Returns:
                    path (str)
        """
        return Audio.get_directory_path_from_path(path) + Audio.get_filename_from_path(path, False)
