from Models.Audio import Audio

audio = Audio()
audio.set_data(b'GkXfo59ChoEBQveBAULygQRC84EIQoKEd2VibUKHgQRC')
audio.change_data_format_from_b64_into_b2()
print(audio.data)
