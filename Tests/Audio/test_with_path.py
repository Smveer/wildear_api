import pytest
from Models.Audio import Audio


@pytest.fixture
def test_path() -> str:
    return "dir1/dir1-1/dir1-1-1/audio.webm"


def test_get_directory_path_from_path(
        test_path: str
):
    assert Audio.get_directory_path_from_path(test_path, True) == "dir1/dir1-1/dir1-1-1/"
    assert Audio.get_directory_path_from_path(test_path, True) != "dir1/dir1-1/dir1-1-1"
    assert Audio.get_directory_path_from_path(test_path) == "dir1/dir1-1/dir1-1-1/"
    assert Audio.get_directory_path_from_path(test_path) != "dir1/dir1-1/dir1-1-1"
    assert Audio.get_directory_path_from_path(test_path, False) == "dir1/dir1-1/dir1-1-1"
    assert Audio.get_directory_path_from_path(test_path, False) != "dir1/dir1-1/dir1-1-1/"
    assert Audio.get_directory_path_from_path(test_path, False) != "dir1/dir1-1/"
    assert Audio.get_directory_path_from_path(test_path, True) != "dir1/dir1-1/"
    assert Audio.get_directory_path_from_path(test_path) != "dir1/dir1-1/"


def test_get_file_extension_from_path(
        test_path: str
):
    assert Audio.get_file_extension_from_path(test_path, True) == ".webm"
    assert Audio.get_file_extension_from_path(test_path, True) != "webm"
    assert Audio.get_file_extension_from_path(test_path) == ".webm"
    assert Audio.get_file_extension_from_path(test_path) != "webm"
    assert Audio.get_file_extension_from_path(test_path, False) == "webm"
    assert Audio.get_file_extension_from_path(test_path, False) != ".webm"
    assert Audio.get_file_extension_from_path(test_path, False) != "audio.webm"
    assert Audio.get_file_extension_from_path(test_path, True) != "audio.webm"
    assert Audio.get_file_extension_from_path(test_path) != "audio.webm"


def test_get_filename_from_path(
        test_path: str
):
    assert Audio.get_filename_from_path(test_path) == "audio.webm"
    assert Audio.get_filename_from_path(test_path) != "audio"
    assert Audio.get_filename_from_path(test_path, True) == "audio.webm"
    assert Audio.get_filename_from_path(test_path, True) != "audio"
    assert Audio.get_filename_from_path(test_path, False) == "audio"
    assert Audio.get_filename_from_path(test_path, False) != "audio.webm"
    assert Audio.get_filename_from_path(test_path, False) != "/audio"
    assert Audio.get_filename_from_path(test_path, False) != "/audio.webm"
    assert Audio.get_filename_from_path(test_path, True) != "/audio.webm"
    assert Audio.get_filename_from_path(test_path, True) != "/audio"
    assert Audio.get_filename_from_path(test_path) != "/audio"
    assert Audio.get_filename_from_path(test_path) != "/audio.webm"


def test_get_path_without_extension_from_path(
        test_path: str
):
    assert Audio.get_path_without_extension_from_path(test_path) == "dir1/dir1-1/dir1-1-1/audio"
    assert Audio.get_path_without_extension_from_path(test_path) != "dir1/dir1-1/dir1-1-1/audio."
