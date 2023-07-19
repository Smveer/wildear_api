import pytest
from Utils.utilities import *


path = "Ressources/Dataset/bear_roar/bear_roar.png"

matrix = flatten_png_file_into_array(str(f), greyscale=True)

"""files = Path(
    Audio.get_directory_path_from_path(path)
).glob(
    Audio.get_filename_from_path(path, False) + "_*" + Audio.get_file_extension_from_path(path)
)

matrixes = [flatten_png_file_into_array(str(f), greyscale=True) for f in files]"""
