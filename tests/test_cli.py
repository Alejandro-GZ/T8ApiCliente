from unittest.mock import patch

import pytest
from click.testing import CliRunner

from t8_client.cli import cli, parse


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()

def test_list_waves(runner: CliRunner) -> None:
    with patch("t8_client.cli.get_wave_list",
               return_value=["t1", "t2"]):

        result = runner.invoke(
            cli,
            ["list-waves", "--machine", "M1", "--point", "P1", "--proc-mode", "raw"]
        )

        assert result.exit_code == 0
        assert "Waveform ISO dates and timestamps" in result.output
        assert "t1" in result.output
        assert "t2" in result.output

def test_list_spectra(runner: CliRunner) -> None:
    with patch("t8_client.cli.get_spectrum_list",
               return_value=["s1"]):

        result = runner.invoke(
            cli,
            ["list-spectra", "-M", "M1", "-p", "P1", "-m", "avg"]
        )

        assert result.exit_code == 0
        assert "Spectra ISO dates" in result.output
        assert "s1" in result.output

def test_get_wave(runner: CliRunner) -> None:
    with patch("t8_client.cli.get_wave_data") as mock_get:

        result = runner.invoke(
            cli,
            ["get-wave", "-M", "M1", "-p", "P1", "-m", "raw", "-t", "123"]
        )

        assert result.exit_code == 0
        mock_get.assert_called_once_with("M1", "P1", "raw", "123")
        assert "Waveform data saved" in result.output

def test_get_spectrum(runner: CliRunner) -> None:
    with patch("t8_client.cli.get_spectrum_data") as mock_get:

        result = runner.invoke(
            cli,
            ["get-spectrum", "--machine", "M1", "--point", "P1",
             "--proc-mode", "avg"]
        )

        assert result.exit_code == 0
        mock_get.assert_called_once()
        assert "Spectra data saved" in result.output

def test_plot_wave(runner: CliRunner) -> None:
    with patch("t8_client.cli.plot_wave_data") as mock_plot:

        result = runner.invoke(
            cli,
            ["plot-wave", "-M", "M1", "-p", "P1", "-m", "raw"]
        )

        assert result.exit_code == 0
        mock_plot.assert_called_once()
        assert "Waveform plot displayed" in result.output

def test_plot_spectrum(runner: CliRunner) -> None:
    with patch("t8_client.cli.plot_spectrum_data") as mock_plot:

        result = runner.invoke(
            cli,
            ["plot-spectrum", "-M", "M1", "-p", "P1", "-m", "avg"]
        )

        assert result.exit_code == 0
        mock_plot.assert_called_once()
        assert "Spectra plot displayed" in result.output

def test_compute_spectrum(runner: CliRunner) -> None:
    with patch("t8_client.cli.compute_and_save_spectrum") as mock_compute:

        result = runner.invoke(
            cli,
            ["compute-spectrum", "--wave", "wave.json"]
        )

        assert result.exit_code == 0
        mock_compute.assert_called_once_with("wave.json")
        assert "Spectrum computed and saved" in result.output

def test_parse_from_path() -> None:
    m, p, pm, ts = parse(None, None, None, "0",
                         "M1:P1:raw:123", None)

    assert (m, p, pm, ts) == ("M1", "P1", "raw", "123")

def test_parse_missing_args() -> None:
    with pytest.raises(Exception):  # noqa: B017
        parse(None, None, None, "0", None, None)

def test_parse_datetime() -> None:
    m, p, pm, ts = parse(
        "M1", "P1", "raw", "0",
        None, "2024-01-01T00:00:00"
    )

    assert isinstance(ts, int)

##### Version 0.1.1 ######
def test_list_procs(runner: CliRunner) -> None:
    mock_procs = {
        "raw": {
            "P1": ["raw"],
            "P2": ["raw"]
        },
        "avg": {
            "P1": ["avg", "avg_10"],
            "P3": ["avg"]
        }
    }

    with patch("t8_client.cli.list_proc_modes",
               return_value=mock_procs):

        result = runner.invoke(
            cli,
            ["list-procs"]
        )

        assert result.exit_code == 0
        assert "Available Processing Modes:" in result.output
        assert "raw" in result.output
        assert "  - P1" in result.output
        assert "  - P2" in result.output
        assert "avg" in result.output
        assert "  - P1" in result.output
        assert "      * avg" in result.output
        assert "      * avg_10" in result.output
        assert "  - P3" in result.output
        assert "      * avg" in result.output
