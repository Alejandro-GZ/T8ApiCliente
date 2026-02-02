import json
import os
from datetime import UTC, datetime
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

from .models.spectra import SpectraData
from .models.waveform import WaveformData


def get_wave_list( machine: str, point: str, proc_mode: str) \
    -> list[str]:
    """
    Retrieve a list of waveform timestamps from the API for a given machine and point.

    This function fetches waveform data from the API endpoint corresponding to the 
    specified `machine`, `point`, and `proc_mode`, and returns a list of timestamps 
    representing available waveform captures.

    Parameters
    ----------
    machine : str
        Identifier of the machine for which to retrieve waveform data.
    point : str
        Measurement point or sensor identifier on the machine.
    proc_mode : str
        Processing mode or data type for the waveform data.

    Returns
    -------
    list[str]
        A list of timestamps (as strings) indicating available waveform records.
    """
    
    timestamps = retrieve_timestamps(fetch(f"waves/{machine}/{point}/{proc_mode}"))
    return timestamps

def get_spectrum_list(machine: str, point: str, proc_mode: str) \
    -> list[str]:
    """
    Retrieve a list of spectral timestamps from the API for a given machine and point.

    This function fetches spectral data from the API endpoint corresponding to the 
    specified `machine`, `point`, and `proc_mode`, and returns a list of timestamps 
    representing available spectral measurements.

    Parameters
    ----------
    machine : str
        Identifier of the machine for which to retrieve spectral data.
    point : str
        Measurement point or sensor identifier on the machine.
    proc_mode : str
        Processing mode or data type for the spectral data.

    Returns
    -------
    list[str]
        A list of timestamps (as strings) indicating available spectral records.
    """
    timestamps = retrieve_timestamps(fetch(f"spectra/{machine}/{point}/{proc_mode}"))
    return timestamps

def get_wave_data(machine: str, point: str, proc_mode: str,
                      timestamp: str=0, save: bool=True) -> dict:
    """
    Retrieve waveform data for a specific timestamp and optionally 
    save it to a JSON file.

    This function fetches waveform data from the API for the specified `machine`, 
    `point`, and `proc_mode`. If `timestamp` is 0, it retrieves the latest available 
    waveform. Optionally, the data can be saved as a JSON file under the `data/waves` 
    directory.

    Parameters
    ----------
    machine : str
        Identifier of the machine for which to retrieve waveform data.
    point : str
        Measurement point or sensor identifier on the machine.
    proc_mode : str
        Processing mode or data type for the waveform data.
    timestamp : str, optional
        Timestamp of the waveform to retrieve. Defaults to 0 (latest waveform).
    save : bool, optional
        Whether to save the retrieved data as a JSON file. Default is True.

    Returns
    -------
    dict
        Dictionary containing the waveform data retrieved from the API.
    """
    data = fetch(f"waves/{machine}/{point}/{proc_mode}/{timestamp}")
    if save:
        save_json_to_file(data, machine, point, proc_mode, timestamp, "wave", 
                      Path("data/waves")) 
    return data

def get_spectrum_data(machine: str, point: str, proc_mode: str, 
                      timestamp: str=0, save: bool=True) -> dict:
    """
    Retrieve spectral data for a specific timestamp and optionally save 
    it to a JSON file.

    This function fetches spectral data from the API for the specified `machine`, 
    `point`, and `proc_mode`. If `timestamp` is 0, it retrieves the latest available 
    spectrum. Optionally, the data can be saved as a JSON file under the `data/spectra` 
    directory.

    Parameters
    ----------
    machine : str
        Identifier of the machine for which to retrieve spectral data.
    point : str
        Measurement point or sensor identifier on the machine.
    proc_mode : str
        Processing mode or data type for the spectral data.
    timestamp : str, optional
        Timestamp of the spectrum to retrieve. Defaults to 0 (latest spectrum).
    save : bool, optional
        Whether to save the retrieved data as a JSON file. Default is True.

    Returns
    -------
    dict
        Dictionary containing the spectral data retrieved from the API.
    """
    data = fetch(f"spectra/{machine}/{point}/{proc_mode}/{timestamp}")
    if save:
        save_json_to_file(data, machine, point, proc_mode, timestamp, "spectrum", 
                      Path("data/spectra"))
    return data

def plot_wave_data(machine: str, point: str, proc_mode: str, 
                      timestamp: str=0) -> None:
    """
    Retrieve and plot waveform data using the WaveformData model.

    This function fetches waveform data from the API for the specified `machine`, 
    `point`, and `proc_mode`. If `timestamp` is 0, it retrieves the latest available 
    waveform. The data is parsed into a `WaveformData` object and plotted using 
    its `plot` method.

    Parameters
    ----------
    machine : str
        Identifier of the machine for which to plot waveform data.
    point : str
        Measurement point or sensor identifier on the machine.
    proc_mode : str
        Processing mode or data type for the waveform data.
    timestamp : str, optional
        Timestamp of the waveform to plot. Defaults to 0 (latest waveform).

    Returns
    -------
    None
    """
    wave_data = get_wave_data(machine, point, proc_mode, timestamp, save=False)
    waveform = WaveformData.parse_obj(wave_data)
    waveform.plot()
    
def plot_spectrum_data(machine: str, point: str, proc_mode: str, 
                      timestamp: str=0) -> None:
    """
    Retrieve and plot spectral data using the SpectraData model.

    This function fetches spectral data from the API for the specified `machine`, 
    `point`, and `proc_mode`. If `timestamp` is 0, it retrieves the latest available 
    spectrum. The data is parsed into a `SpectraData` object and plotted using 
    its `plot` method.

    Parameters
    ----------
    machine : str
        Identifier of the machine for which to plot spectral data.
    point : str
        Measurement point or sensor identifier on the machine.
    proc_mode : str
        Processing mode or data type for the spectral data.
    timestamp : str, optional
        Timestamp of the spectrum to plot. Defaults to 0 (latest spectrum).

    Returns
    -------
    None
    """
    spectrum_data = get_spectrum_data(machine, point, proc_mode, timestamp, save=False)
    spectra = SpectraData.parse_obj(spectrum_data)
    spectra.plot()

def compute_and_save_spectrum(wave_file: str) -> None:
    """
    Compute the spectrum from a waveform file and save it as a JSON file.

    This function reads a waveform from a JSON file, parses it into a 
    `WaveformData` object, and extracts the machine, point, processing mode, 
    and timestamp. It then retrieves spectral parameters from the API, computes 
    the spectrum within the specified frequency range using the waveform's 
    `compute_spectrum` method, and organizes the frequency and amplitude data 
    into a dictionary. Finally, the spectrum data is saved as a JSON file under 
    the `data/spectra` directory with a flag indicating it was computed locally.

    Parameters
    ----------
    wave_file : str
        Path to the JSON file containing the waveform data.

    Returns
    -------
    None
    """
    waveform: WaveformData = WaveformData.parse_obj(json.load(open(wave_file)))
    machine, point, proc_mode = waveform.path.split(":") \
        if ":" in waveform.path else ("unknown", "unknown", "unknown")
    timestamp = int(waveform.snap_t) if waveform.snap_t is not None \
        and waveform.snap_t != "" else 0
    
    # Fetching del espectro
    api_spectr = get_spectrum_data(machine=machine,
                                  point=point, 
                                  proc_mode=proc_mode, 
                                  timestamp=timestamp,
                                  save=False)
    # Computación del espectro
    spectra: tuple = waveform.compute_spectrum(
        fmin=api_spectr["min_freq"], 
        fmax=api_spectr["max_freq"]) # Tupla frecuencia espectro
    # Organizar data
    data = {
        "frequencies": spectra[0].tolist(),
        "amplitudes": spectra[1].tolist(),
        "min_freq": api_spectr["min_freq"],
        "max_freq": api_spectr["max_freq"],
    }
    
    # Save spectrum data to JSON file
    save_json_to_file(
        data=data,
        machine=machine,
        point=point,
        proc_mode=proc_mode,
        timestamp=timestamp,
        type="spectrum",
        output_dir=Path("data/spectra"),
        is_computed=True
    )

# Helper functions
def get_base_url()-> str:
    """Reads the base URL from environment variables."""
    return os.getenv("T8_HOST", "valor_por_defecto")

def get_auth()-> HTTPBasicAuth:
    return HTTPBasicAuth(os.getenv("T8_USER"), os.getenv("T8_PASSWORD"))

def fetch(path: str) -> dict:
    """Fetch data from the given API path."""
    response = requests.get(f"{get_base_url()}/{path}", auth=get_auth())
    response.raise_for_status()
    return response.json()

def retrieve_timestamps(json_response: dict) -> list[str]:
    """Extract timestamps from the JSON response."""
    items = json_response["_items"]
    timestamps = [ format_item(item)
                  for item in items]
    return timestamps
    
def format_item(item: dict) -> str:
    """ Format a timestamp from a dictionary item into a string 
    with ISO date and raw timestamp. """
    ts_str = item["_links"]["self"].split("/")[-1] 
    ts_val = float(ts_str)
    if(ts_val == 0):
        return "[latest / 0]"
    dt_obj = datetime.fromtimestamp(ts_val, tz=UTC)

    iso_date = dt_obj.isoformat()
    
    return f"[{iso_date} / {ts_str}]"

def save_json_to_file(data: dict, machine: str, point: str, proc_mode: str, 
                      timestamp: str, type: str, output_dir: Path, 
                      is_computed: bool=False) -> None:
    """Save JSON data to a specified file path."""
    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to JSON file
    filename = f"{type}_{machine}_{point}_{proc_mode}_{timestamp}"
    filename += "_computed" if is_computed else "" 
    filename += ".json"
    filepath = f"{output_dir}/{filename}"
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)