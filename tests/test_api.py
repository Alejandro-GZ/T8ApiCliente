from unittest.mock import MagicMock, patch

import numpy as np

from t8_client.api import (
    compute_and_save_spectrum,
    get_spectrum_data,
    get_spectrum_list,
    get_wave_data,
    get_wave_list,
    plot_spectrum_data,
    plot_wave_data,
)
from t8_client.models import SpectraData, WaveformData
from t8_client.models.config import ProcMode


def test_get_wave_list()->None:
    fake_json = {
        "data": [
            {"timestamp": "t1"},
            {"timestamp": "t2"},
        ]
    }

    with patch("t8_client.api.get_base_url", return_value="http://api"), \
         patch("t8_client.api.fetch", return_value=fake_json), \
         patch("t8_client.api.retrieve_timestamps",
               return_value=["t1", "t2"]):

        result = get_wave_list("M1", "P1", "raw")

        assert result == ["t1", "t2"]

def test_get_spectrum_list()->None:
    fake_json = {
        "data": [
            {"timestamp": "s1"},
            {"timestamp": "s2"},
        ]
    }

    with patch("t8_client.api.get_base_url", return_value="http://api"), \
         patch("t8_client.api.fetch", return_value=fake_json), \
         patch("t8_client.api.retrieve_timestamps",
               return_value=["s1", "s2"]):

        result = get_spectrum_list("M1", "P1", "avg")

        assert result == ["s1", "s2"]

def test_get_wave_data_latest_and_save()->None:
    fake_data = {"wave": [1, 2, 3]}

    with patch("t8_client.api.fetch", return_value=fake_data), \
         patch("t8_client.api.get_wave_list",
               return_value=["t1", "t2"]), \
         patch("t8_client.api.save_json_to_file") as mock_save:

        result = get_wave_data(
            "M1", "P1", "raw",
            timestamp=0,
            save=True
        )

        assert result == fake_data
        mock_save.assert_called_once()

def test_get_wave_data_no_save()->None:
    fake_data = {"wave": [4, 5, 6]}

    with patch("t8_client.api.fetch", return_value=fake_data), \
         patch("t8_client.api.save_json_to_file") as mock_save:

        result = get_wave_data(
            "M1", "P1", "raw",
            timestamp="t1",
            save=False
        )

        assert result == fake_data
        mock_save.assert_not_called()

def test_get_spectrum_data()->None:
    fake_data = {"spectrum": [10, 20, 30]}

    with patch("t8_client.api.fetch", return_value=fake_data), \
         patch("t8_client.api.get_spectrum_list",
               return_value=["s1", "s2"]), \
         patch("t8_client.api.save_json_to_file") as mock_save:

        result = get_spectrum_data(
            "M1", "P1", "avg",
            timestamp=0,
            save=True
        )

        assert result == fake_data
        mock_save.assert_called_once()

def test_plot_wave_data()->None:
    fake_wave = {"wave": [1, 2, 3]}

    with patch("t8_client.api.get_wave_data",
               return_value=fake_wave), \
         patch("t8_client.models.WaveformData.parse_obj",
               return_value=WaveformData(
                    links="",
                    factor="",
                    snap_t="",
                    speed="",
                    unit_id="",
                    path="",
                    t="",
                    sample_rate="",
                    data=""
                )), \
         patch("t8_client.models.WaveformData.plot") as mock_model:

        plot_wave_data("M1", "P1", "raw")

        mock_model.assert_called_once_with()

def test_plot_spectrum_data()->None:
    fake_spectrum = {"spectrum": [10, 20]}

    with patch("t8_client.api.get_spectrum_data",
               return_value=fake_spectrum), \
         patch("t8_client.models.SpectraData.parse_obj",
               return_value=SpectraData(
                    links="",
                    factor="",
                    snap_t="",
                    speed="",
                    unit_id="",
                    path="",
                    t="",
                    max_freq="",
                    min_freq="",
                    window="",
                    data=""
                )), \
         patch("t8_client.models.SpectraData.plot") as mock_model:

        plot_spectrum_data("M1", "P1", "avg")

        mock_model.assert_called_once_with()

def test_compute_and_save_spectrum()->None:
    fake_spectrum = {"freq": [1, 2], "amp": [10, 20],
                     "max_freq":2, "min_freq":1}
    fake_computed_spectrum = (np.array([1, 2]), np.array([10, 20]))

    with patch("t8_client.api.fetch", return_value={"wave": [1, 2, 3]}), \
         patch("t8_client.api.get_spectrum_data", return_value=fake_spectrum), \
         patch("json.load", return_value={"wave": [1, 2, 3]}), \
         patch("t8_client.models.WaveformData.parse_obj",
               return_value=WaveformData(
                    links="",
                    factor="",
                    snap_t="",
                    speed="",
                    unit_id="",
                    path="",
                    t="",
                    sample_rate="",
                    data=""
                )), \
         patch("t8_client.api.get_proc_mode",
               return_value=ProcMode(
                    name="",
                    max_freq=2,
                    min_freq=1
                )), \
         patch("t8_client.models.WaveformData.compute_spectrum",
               return_value=fake_computed_spectrum), \
         patch("t8_client.api.save_json_to_file") as mock_save, \
         patch("builtins.open", new_callable=MagicMock):

        compute_and_save_spectrum("wave_MAC_POI_PROCM_0.json")

        mock_save.assert_called_once()
