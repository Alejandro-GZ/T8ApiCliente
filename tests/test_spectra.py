from unittest.mock import patch

import numpy as np
import pytest

from t8_client.models.config import Unit
from t8_client.models.spectra import SpectraData


@pytest.fixture
def spectra() -> SpectraData:
    return SpectraData(
        links={},
        factor=1.0,
        snap_t=0,
        speed=0,
        unit_id="unit",
        path="M1:P1:avg",
        t=123456,
        max_freq=500.0,
        min_freq=0.0,
        window=1024,
        data=b"\x01\x02\x03\x04"
    )

def test_plot_calls_plot_xy(spectra: SpectraData) -> None:
    fake_spec = np.array([10, 20, 30, 40], dtype=np.int16)

    with patch.object(spectra, "decode", return_value=fake_spec), \
         patch("t8_client.models.spectra.plot_xy") as mock_plot:

        spectra.plot(Unit(property_name="Amplitude", label="V",
                          id=-1,factor=1.0,property_label=""))

        mock_plot.assert_called_once()

        args, kwargs = mock_plot.call_args

        # Eje X (frecuencia)
        freq = kwargs["x"]
        assert len(freq) == len(fake_spec)
        assert freq[0] == spectra.min_freq
        assert freq[-1] == spectra.max_freq

        # Eje Y (magnitud)
        assert kwargs["y"].tolist() == fake_spec.tolist()

        assert kwargs["xlabel"] == "Frequency (Hz)"
        assert kwargs["ylabel"] == "Amplitude(V)"
        assert "Spectra for path" in kwargs["title"]

def test_parse_obj() -> None:
    data = {
        "_links": {},
        "factor": 2.0,
        "snap_t": 1,
        "speed": 100,
        "unit_id": "unit",
        "path": "M1:P1:avg",
        "t": 999,
        "max_freq": 1000.0,
        "min_freq": 0.0,
        "window": 2048,
        "data": b"\x00\x01",
    }

    obj = SpectraData.parse_obj(data)

    assert isinstance(obj, SpectraData)
    assert obj.path == "M1:P1:avg"
    assert obj.max_freq == 1000.0
    assert obj.min_freq == 0.0
    assert obj.window == 2048
    assert obj.t == 999

