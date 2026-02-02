from unittest.mock import patch

import numpy as np
import pytest

from t8_client.models.waveform import WaveformData


@pytest.fixture
def waveform() -> WaveformData:
    return WaveformData(
        links={},
        factor=1.0,
        snap_t=0,
        speed=0,
        unit_id="unit",
        path="M1:P1:raw",
        t=123456,
        sample_rate=1000,
        data=b"\x01\x02\x03\x04"
    )

def test_plot_calls_plot_xy(waveform: WaveformData) -> None:
    fake_signal = np.array([1, 2, 3, 4], dtype=np.int16)

    with patch.object(waveform, "decode", return_value=fake_signal), \
         patch("t8_client.models.waveform.plot_xy") as mock_plot:

        waveform.plot()

        mock_plot.assert_called_once()

        args, kwargs = mock_plot.call_args
        assert kwargs["xlabel"] == "Time [s]"
        assert kwargs["ylabel"] == "Amplitude"
        assert "Waveform for signal path" in kwargs["title"]
        assert kwargs["y"].tolist() == fake_signal.tolist()

def test_compute_spectrum_basic(waveform: WaveformData) -> None:
    sample_rate = waveform.sample_rate
    t = np.linspace(0, 1, sample_rate, endpoint=False)
    signal = np.sin(2 * np.pi * 50 * t)

    with patch.object(waveform, "decode", return_value=signal):

        freqs, spectrum = waveform.compute_spectrum(40, 60)

        assert len(freqs) > 0
        assert np.all(freqs >= 40)
        assert np.all(freqs <= 60)
        assert spectrum.max() > 0

def test_compute_spectrum_out_of_range(waveform: WaveformData) -> None:
    signal = np.zeros(1000)

    with patch.object(waveform, "decode", return_value=signal):

        freqs, spectrum = waveform.compute_spectrum(100, 200)

        assert freqs.size == 101
        assert spectrum.size == 101

def test_parse_obj() -> None:
    data = {
        "_links": {},
        "factor": 1.0,
        "snap_t": 0,
        "speed": 0,
        "unit_id": "unit",
        "path": "M1:P1:raw",
        "t": 123,
        "sample_rate": 1000,
        "data": b"\x00\x01",
    }

    obj = WaveformData.parse_obj(data)

    assert isinstance(obj, WaveformData)
    assert obj.sample_rate == 1000
    assert obj.path == "M1:P1:raw"
    assert obj.t == 123
