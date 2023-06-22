from Models.Audio import Audio
import pytest


@pytest.fixture
def test_audio() -> Audio:
    a = Audio()
    a.path = "a"
    a.data = "d"
    a.encoding = "e"
    return a


@pytest.fixture
def test_duplicate() -> Audio:
    o = Audio()
    o.path = "a"
    o.data = "d"
    o.encoding = "e"
    return o


@pytest.fixture
def test_other() -> Audio:
    o2 = Audio()
    o2.path = "a"
    o2.data = "b"
    o2.encoding = "e"
    return o2


def test___eq__(
        test_audio: Audio,
        test_duplicate: Audio,
        test_other: Audio
):
    assert test_audio == test_duplicate
    assert test_audio != test_other
