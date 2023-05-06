import subprocess
import os
from pydub import AudioSegment
from Models.Audio import Audio

# for data transformation
import numpy as np
# for visualizing the data
import matplotlib.pyplot as plt
# for opening the media file
import scipy.io.wavfile as wavfile

"""
    Create .webm file with binary sound
"""


def create_webm(audio: Audio):
    directory_path = audio.get_directory_path_from_path()

    # Check if the directory exists, else create one
    if os.path.isdir(directory_path) is False:
        os.mkdir(directory_path)

    # Write content inside audio into a file
    with open(audio.path, "wb") as f:
        f.write(audio.data)

    f.close()


"""
    1 - Convert .webm file to .wav file with ffmpeg
    2 - Convert stereo to mono
    3 - Fix audio duration to 5 seconde
"""


def convert_webm_to_wav(audio: Audio):
    new_path = audio.get_directory_path_from_path() + "/" + audio.get_filename_from_path(False) + ".wav"

    # Convert with ffmpeg utility thanks to a subprocess
    subprocess.run(
        ["ffmpeg", "-y", "-i", audio.path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", new_path])

    # Delete old file from audio path
    os.remove(audio.path)

    # Set new path to the audio
    audio.set_path(new_path)

    # Convert the audio from stereo(2) to mono(1)
    sound = convert_stereo_to_mono(audio)

    # Set optimal duration of 5s (5000 ms)
    optimal_duration = 5000

    # Get current sounds duration
    current_duration = len(sound)

    # If current duration is higher than the optimal, cut to optimize current sound
    if current_duration > optimal_duration:
        sound = sound[:optimal_duration]
    # If current duration is lower than the optimal, complete with silent noise
    elif current_duration < optimal_duration:
        silence = AudioSegment.silent(duration=optimal_duration - current_duration)
        sound = sound + silence

    # Export audio with his extension
    sound.export(audio.path, format=audio.get_file_extension_from_path())
    return audio


"""
    Convert stereo chanel (2) to Mono channel (1) - usefull for spectogram
"""


def convert_stereo_to_mono(audio: Audio):
    return AudioSegment.from_wav(audio.path).set_channels(1)


"""
    1 - Get an audio and cut into segments of 0,5s 
    2 - Delete .wav file
"""


def create_image_segments_from_audio(audio: Audio):
    # Put matplotlib figure image at 50px*50px
    plt.figure(figsize=(0.5, 0.5))  # -> 1px = 0.01
    # We don"t want to see axis, so we turn off axis
    plt.axis("off")

    # Get sound from file
    sound = AudioSegment.from_wav(audio.path)

    # Divide file into pieces (1 element = 1 ms => here 500 ms = 500 elements)
    pieces = sound[::500]

    # Save each piece into a file
    i = 1
    for piece in pieces:
        # Create path for file thanks to i
        path = audio.get_directory_path_from_path() + "/" + audio.get_filename_from_path(False) + "_" + str(i) + "."

        # Create file for audio segment
        piece.export(path + audio.get_file_extension_from_path(), format=audio.get_file_extension_from_path())

        # After creating audio file, read file to get information
        audio_rate, audio_data = wavfile.read(path + audio.get_file_extension_from_path())

        # Delete audio file, we don"t need it again
        os.remove(path + audio.get_file_extension_from_path())

        # Create spectrogram thanks to audio information received just before
        plt.specgram(audio_data, Fs=audio_rate)

        # Save file with png extension
        plt.savefig(path + "png")

        # increment to save next piece name file
        i += 1

    # Delete the original .wav file (non-segmented one)
    os.remove(audio.path)
