from Models.Audio import Audio

audio = Audio()
audio.set_path("dir1/dir1-1/dir1-1-1/audio.webm")

print(audio.get_directory_path_from_path())