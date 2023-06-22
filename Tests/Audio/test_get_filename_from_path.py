from Models.Audio import Audio

print(Audio.get_filename_from_path("dir1/dir1-1/dir1-1-1/audio.webm"))
print(Audio.get_filename_from_path("dir1/dir1-1/dir1-1-1/audio.webm", extension=False))
