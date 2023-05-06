import subprocess
import os
from pydub import AudioSegment
from Models.Audio import Audio

"""
    Create .webm file with binary sound
"""
def create_webm(audio: Audio):
    audio.set_path("Data/audio.webm")
    with open(audio.path, "wb") as f:
        f.write(audio.data)
    f.close()
    return audio

"""
    1 - Convert .webm file to .Wav file with ffmpeg
    2 - Convert stereo to mono
    3 - Fix audio duration to 5 seconde
"""
def convert_webm_to_wav(audio: Audio):
    # Conversion avec ffmpeg
    subprocess.run(["ffmpeg", "-i", audio.path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", "Data/audio.wav"])

    # Supprime le fichier .webm
    os.remove(audio.path)

    # Change the path to the .wav
    audio.set_path("Data/audio.wav")

    # Convertie le channel stereo(2) en mono(1) pour création spectrogramme
    sound = convert_stereo_to_mono(audio)

    # Fixer la durée à 5 seconde (5 000 ms)
    duration_optimal = 5000

    # Récupérer la durée actuelle
    current_duration = len(sound)
    
    # Si la durée actuelle est supérieure à la nouvelle durée, couper le son
    if current_duration > duration_optimal:
        sound = sound[:duration_optimal]
    # Si la durée actuelle est inférieure à la nouvelle durée, ajouter du silence
    elif current_duration < duration_optimal:
        silence = AudioSegment.silent(duration = duration_optimal - current_duration)
        sound = sound + silence

    # Export l'audio
    sound.export("Data/audio.wav", format="wav")

    return audio

"""
    Convert stereo chanel (2) to Mono channel (1) usefull for spectogram
"""
def convert_stereo_to_mono(audio: Audio):
    return AudioSegment.from_wav(audio.path).set_channels(1)

"""
    1 - Get the audio (5s) and cut it to 10 segments of 0,5s 
    2 - Delete .wav file
"""
def create_segments(audio : Audio):
    # Charger le fichier audio en mono
    sound = AudioSegment.from_wav(audio.path)

    # Diviser le fichier audio en parties
    parts = sound[::500]

    # Sauvegarder chaque partie dans un fichier
    i = 0
    for part in parts:
        part.export(f"Data/segment_{i}.wav", format="wav")
        i += 1

    # Delete the original .wav file
    os.remove(audio.path)

def get_file_name_from_path(audio: Audio):
    return audio.path.split("/")[-1]