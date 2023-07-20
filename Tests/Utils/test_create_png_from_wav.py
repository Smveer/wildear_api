from Utils.utilities import *


path = "Dataset/Sounds/bear_roar/bear_roar.wav"

files = Path(
    Audio.get_directory_path_from_path(path)
).glob(
    Audio.get_filename_from_path(path, False) + "_*" + Audio.get_file_extension_from_path(path)
)

for f in files:
    create_png_from_wav(str(f), replace=False)
