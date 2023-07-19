
import os
import ctypes
import subprocess
import numpy as np
from PIL import Image
from pathlib import Path
from numpy import ndarray
from pydub import AudioSegment
from Models.Audio import Audio
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile


def create_file_from_audio(
        audio: Audio
):
    """
    Create audio media file from Audio instance:

        Parameters:
                    audio (Audio): audio containing data that will fill the file created
    """
    directory_path = Audio.get_directory_path_from_path(audio.path)

    # Check if the directory exists, else create one
    if os.path.isdir(directory_path) is False:
        os.mkdir(directory_path)

    # Write content inside audio into a file
    with open(audio.path, "wb") as f:
        f.write(audio.data)

    f.close()


def create_wav_audio_from_webm_audio(
        audio: Audio,
        optimum: int = -1,
        replace: bool = False
) -> Audio:
    """
    Use Audio instance to convert webm file into wav file,\n
    use optimum to cut the audio for a certain size,\n
    and replace webm file if desired.

        Parameters:
                    audio (Audio): Audio instance with webm file path
                    optimum (int): in milliseconds, -1 per default, it means it doesn't cut the sound
                    replace (bool): False as default, will delete webm file if True
        Returns:
                audio (Audio): new Audio instance with new path of wav file
    """
    new_path = Audio.get_directory_path_from_path(audio.path) + Audio.get_filename_from_path(audio.path, False) + ".wav"

    subprocess.run(  # Convert with ffmpeg utility (installed manually) thanks to a subprocess
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

    sound.export(
        audio.path,
        format=Audio.get_file_extension_from_path(audio.path, False)
    )  # Export audio with his extension

    return audio


def get_mono_channel_sound_segments_from_wav(
        path
) -> list:
    """
    Return list of wav audio segments in mono channel

        Parameters:
                    path (str): path of the wav to retrieve segments
        Returns:
                segments (list): list of audio segments (each element is one millisecond of audio)
    """
    return AudioSegment.from_wav(path).set_channels(1)


def create_png_from_wav(
        path: str,
        size_x: float = 0.5,
        size_y: float = 0.5,
        axis: bool = False,
        replace: bool = False
):
    """
    Create png image from audio file (type wav), scale image with xy, hide/unhide axis on it, delete audio file after.

        Parameters:
                    path (str): path of the audio to transform
                    size_x (float): 0.5 as default, x side of image, 0.01 => 1 pixel
                    size_y (float): 0.5 as default, y side of image, 0.01 => 1 pixel
                    axis (bool): False as default, hide (False) unhide(True) axis
                    replace (bool): False as default, if True delete file after image creation
    """
    audio_rate, audio_data = wavfile.read(path)  # Read file to get information

    axis = "on" if axis else "off"

    if size_x < 0 or size_y < 0:
        size_x, size_y = 0.5, 0.5

    plt.figure(figsize=(size_x, size_y))  # -> 1px = 0.01
    plt.axis(axis)  # Turn on or off axis
    plt.specgram(audio_data, Fs=audio_rate)  # Create spectrogram thanks to audio information received just before
    plt.savefig(Audio.get_path_without_extension_from_path(path) + ".png")  # Save file with png extension
    plt.close()  # Close plot file

    if replace:
        # Delete audio file if replace is True
        os.remove(path)


def create_pieces_from_wav(
        path: str,
        size_in_milliseconds: int = 500,
        replace: bool = False
):
    """
    Create png image from audio file (type wav), scale image with xy, hide/unhide axis on it, delete audio file after.

        Parameters:
                    path (str): path of the audio to cut into pieces
                    size_in_milliseconds (int): 500 as default, size of each piece, 500 => 0.5 second
                    replace (bool): False as default, if True delete original file after all cuts
    """
    size_in_milliseconds = 500 if size_in_milliseconds < 0 else size_in_milliseconds

    sound = get_mono_channel_sound_segments_from_wav(path)  # Get sound segments from file, 1 segment = 1 ms
    pieces = sound[::size_in_milliseconds]  # Divide sound into pieces of size_in_milliseconds size

    for i, piece in enumerate(pieces):
        piece.export(  # Export piece as sound, same time than the original
            Audio.get_path_without_extension_from_path(path) + "_" + str(i) + Audio.get_file_extension_from_path(path),
            format=Audio.get_file_extension_from_path(  # Not necessary but exports are faster when format is specified
                path,
                False
            )
        )

    if replace:
        # Delete audio file if replace is True
        os.remove(path)


def flatten_png_file_into_array(
        file_path: str,
        greyscale: bool = True
) -> ndarray:
    """
    Return a 2D array of pixels from a png file

        Parameters:
                    file_path (str): path of the png file to flatten
                    greyscale (bool): True as default, if True return greyscale array, else return RGB array
        Returns:
                array (list): array of pixels
    """
    image = Image.open(file_path)
    i = np.array(image.convert('L'), dtype=np.float32) if greyscale else np.array(image, dtype=np.float32)
    print(i)
    image.close()
    return i


def treat_wav_for_wildear(
        path: str,
        replace: bool = True
) -> list:
    """
    Create png images after cutting the wav file in the Wild Ear way

        Parameters:
                    path (str): path of the audio to transform into images
                    replace (bool): True as default, if True delete original files after all transformations
    """
    create_pieces_from_wav(path, replace)

    files = Path(
        Audio.get_directory_path_from_path(path)
    ).glob(
        Audio.get_filename_from_path(path, False) + "_*" + Audio.get_file_extension_from_path(path)
    )

    for f in files:
        create_png_from_wav(str(f), replace)
        yield flatten_png_file_into_array(
            str(f).replace(Audio.get_file_extension_from_path(path), ".png"))


def rust_ptr_to_np_array(
        rust_ptr: ctypes.POINTER(ctypes.c_float),
        size: int
) -> ndarray:
    """
    Return a numpy array from a rust pointer
        parameters:
                    rust_ptr (ctypes.POINTER(ctypes.c_float)): pointer to a rust array
                    size (int): size of the array
        returns:
                np_array (ndarray): numpy array
    """
    np_array = np.zeros(size, dtype=np.float32)
    for i in range(size):
        np_array[i] = rust_ptr[i]
    return np_array
