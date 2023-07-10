import pytest
from Utils.utilities import *


@pytest.fixture
def path():
    return "/Users/manwis/Desktop/ESGI3IABD2/PA/API/Tests/Utils/green.png"


def test_flatten_png_file_into_array(
        path: str
):
    flatten_png_file_into_array(path, greyscale=True)
