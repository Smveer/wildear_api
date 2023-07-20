from Utils.utilities import *


path = "red.png"

matrix = flatten_png_file_into_array(path, greyscale=True)

print(matrix)

"""files = Path(
    Audio.get_directory_path_from_path(path)
).glob(
    Audio.get_filename_from_path(path, False) + "_*" + Audio.get_file_extension_from_path(path)
)

matrixes = [flatten_png_file_into_array(str(f), greyscale=True) for f in files]"""
