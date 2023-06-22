from Models.Audio import Audio
import pytest


@pytest.fixture
def audio_in_b2() -> Audio:
    audio = Audio()
    audio.set_encoding("b2")
    audio.set_data(b'\x1aE\xdf\xa3\x9fB\x86\x81\x01B\xf7\x81\x01B\xf2\x81\x04B\xf3\x81\x08B\x82\x84webmB\x87\x81\x04B')
    return audio


@pytest.fixture
def audio_in_b64() -> Audio:
    audio = Audio()
    audio.set_encoding("b64")
    audio.set_data(b'GkXfo59ChoEBQveBAULygQRC84EIQoKEd2VibUKHgQRC')
    return audio


def test_change_data_format_from_b2_into_b64(
        audio_in_b2: Audio,
        audio_in_b64: Audio,
):
    audio_in_b2.change_data_format_from_b2_into_b64()
    assert audio_in_b2 == audio_in_b64


def test_change_data_format_from_b64_into_b2(
        audio_in_b2: Audio,
        audio_in_b64: Audio,
):
    audio_in_b64.change_data_format_from_b64_into_b2()
    assert audio_in_b64 == audio_in_b2
