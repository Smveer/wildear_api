from Models.Audio import Audio

audio = Audio()
audio.set_data(b'\x1aE\xdf\xa3\x9fB\x86\x81\x01B\xf7\x81\x01B\xf2\x81\x04B\xf3\x81\x08B\x82\x84webmB\x87\x81\x04B')

audio.change_data_format_from_b2_into_b64()
print(audio.data)
