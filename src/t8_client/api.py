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
    """Retrieve a list of waveform timestamps from the API."""
    
    timestamps = retrieve_timestamps(fetch(f"waves/{machine}/{point}/{proc_mode}"))
    return timestamps

def get_spectrum_list(machine: str, point: str, proc_mode: str) \
    -> list[str]:
    """Retrieve a list of spectra timestamps from the API."""
    timestamps = retrieve_timestamps(fetch(f"spectra/{machine}/{point}/{proc_mode}"))
    return timestamps

def get_wave_data(machine: str, point: str, proc_mode: str,
                      timestamp: str=0, save: bool=True) -> dict:
    """Retrieve waveform data for a specific timestamp and save to JSON file.
       If timestamp is 0, retrieves the latest waveform.
    """
    data = fetch(f"waves/{machine}/{point}/{proc_mode}/{timestamp}")
    if save:
        save_json_to_file(data, machine, point, proc_mode, timestamp, "wave", 
                      Path("data/waves")) 
    return data

def get_spectrum_data(machine: str, point: str, proc_mode: str, 
                      timestamp: str=0, save: bool=True) -> dict:
    """Retrieve spectra data for a specific timestamp and save to JSON file.
       If timestamp is 0, retrieves the latest spectra.
    """
    data = fetch(f"spectra/{machine}/{point}/{proc_mode}/{timestamp}")
    if save:
        save_json_to_file(data, machine, point, proc_mode, timestamp, "spectrum", 
                      Path("data/spectra"))
    return data

def plot_wave_data(machine: str, point: str, proc_mode: str, 
                      timestamp: str=0) -> None:
    """Plot waveform data using the WaveformData model."""
    wave_data = get_wave_data(machine, point, proc_mode, timestamp, save=False)
    waveform = WaveformData.parse_obj(wave_data)
    waveform.plot()
    
def plot_spectrum_data(machine: str, point: str, proc_mode: str, 
                      timestamp: str=0) -> None:
    """Plot spectra data using the SpectraData model."""
    spectrum_data = get_spectrum_data(machine, point, proc_mode, timestamp, save=False)
    spectra = SpectraData.parse_obj(spectrum_data)
    spectra.plot()

def compute_and_save_spectrum(wave_file: str) -> None:
    """Compute and save spectrum from a waveform file."""
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
    """Lee la variable de entorno en tiempo de ejecución, no al importar"""
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