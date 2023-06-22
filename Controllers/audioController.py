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


def create_webm_from_audio(audio: Audio):
    directory_path = Audio.get_directory_path_from_path(audio.path)

    # Check if the directory exists, else create one
    if os.path.isdir(directory_path) is False:
        os.mkdir(directory_path)

    # Write content inside audio into a file
    with open(audio.path, "wb") as f:
        f.write(audio.data)

    f.close()


"""
    Convert stereo chanel (2) to Mono channel (1) - usefull for spectogram
"""


def get_mono_channel_sound_segments_from_wav(path):
    return AudioSegment.from_wav(path).set_channels(1)


"""
    1 - Convert .webm file to .wav file with ffmpeg
    2 - Convert stereo to mono
    3 - Fix audio duration to 5 secondes
"""


def convert_webm_to_wav(audio: Audio, optimum: int = 5000, replace: bool = False):
    new_path = Audio.get_directory_path_from_path(audio.path) + "/" + Audio.get_filename_from_path(audio.path, False)
    new_path += ".wav"

    subprocess.run(  # Convert with ffmpeg utility thanks to a subprocess
        [
            "ffmpeg",
            "-y",
            "-i",
            audio.path,
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "44100",
            "-ac",
            "2",
            new_path
        ]
    )

    if replace:
        os.remove(audio.path)  # Delete old file if replace == True

    audio.set_path(new_path)  # Set new path to the audio

    sound = get_mono_channel_sound_segments_from_wav(audio.path)  # Convert the audio from stereo(2) to mono(1)

    if optimum > 0:
        optimal_duration = optimum
        current_duration = len(sound)  # Get current sounds duration
        if current_duration > optimal_duration:  # If current duration is higher than the optimal,
            sound = sound[:optimal_duration]  # cut to optimize current sound
        elif current_duration < optimal_duration:  # If current duration is lower than the optimal,
            silence = AudioSegment.silent(duration=optimal_duration - current_duration)
            sound = sound + silence  # complete with silent noise

    sound.export(audio.path, format=Audio.get_file_extension_from_path(audio.path))  # Export audio with his extension
    return audio


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
        path = Audio.get_directory_path_from_path(audio.path) + "/" + Audio.get_filename_from_path(audio.path, False)
        path += "_" + str(i) + "."

        # Create file for audio segment
        piece.export(path + Audio.get_file_extension_from_path(audio.path), format=Audio.get_file_extension_from_path(audio.path))

        # After creating audio file, read file to get information
        audio_rate, audio_data = wavfile.read(path + Audio.get_file_extension_from_path(audio.path))

        # Delete audio file, we don"t need it again
        os.remove(path + Audio.get_file_extension_from_path(audio.path))

        # Create spectrogram thanks to audio information received just before
        plt.specgram(audio_data, Fs=audio_rate)

        # Save file with png extension
        plt.savefig(path + "png")

        # increment to save next piece name file
        i += 1

    # Delete the original .wav file (non-segmented one)
    os.remove(audio.path)
