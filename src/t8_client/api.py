import json
import os
from datetime import UTC, datetime
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

from .models.spectra import SpectraData
from .models.waveform import WaveformData

USERNAME = os.getenv("T8_USER", "")
PASSWORD = os.getenv("T8_PASSWORD", "")
BASE_URL = os.getenv("T8_HOST", "")
AUTH = HTTPBasicAuth(USERNAME, PASSWORD)

def get_wave_list( machine: str, point: str, proc_mode: str) \
    -> list[str]:
    """Retrieve a list of waveform timestamps from the API."""
    response = requests.get(
        f"{BASE_URL}/waves/{machine}/{point}/{proc_mode}", auth=AUTH)
    response.raise_for_status()
    timestamps = retrieve_timestamps(response.json())
    return timestamps

def get_spectrum_list(machine: str, point: str, proc_mode: str) \
    -> list[str]:
    """Retrieve a list of spectra timestamps from the API."""
    response = requests.get(
        f"{BASE_URL}/spectra/{machine}/{point}/{proc_mode}", auth=AUTH)
    response.raise_for_status()
    timestamps = retrieve_timestamps(response.json())
    return timestamps

def get_wave_data(machine: str, point: str, proc_mode: str,
                      timestamp: str=0) -> dict:
    """Retrieve waveform data for a specific timestamp and save to JSON file.
       If timestamp is 0, retrieves the latest waveform.
    """
    
    response = requests.get(
        f"{BASE_URL}/waves/{machine}/{point}/{proc_mode}/{timestamp}", auth=AUTH)
    response.raise_for_status()
    
    data = response.json()
    save_json_to_file(data, machine, point, proc_mode, timestamp, "wave", 
                      Path("data/waves"))
    
    return data

def get_spectrum_data(machine: str, point: str, proc_mode: str, 
                      timestamp: str=0) -> dict:
    """Retrieve spectra data for a specific timestamp and save to JSON file.
       If timestamp is 0, retrieves the latest spectra.
    """
    
    response = requests.get(
        f"{BASE_URL}/spectra/{machine}/{point}/{proc_mode}/{timestamp}", auth=AUTH)
    response.raise_for_status()
    
    data = response.json()
    save_json_to_file(data, machine, point, proc_mode, timestamp, "spectrum", 
                      Path("data/spectra"))

    return data

def plot_wave_data(machine: str, point: str, proc_mode: str, 
                      timestamp: str=0) -> None:
    """Plot waveform data using the WaveformData model."""
    wave_data = get_wave_data(machine, point, proc_mode, timestamp)
    waveform = WaveformData.parse_obj(wave_data)
    waveform.plot()
    
def plot_spectrum_data(machine: str, point: str, proc_mode: str, 
                      timestamp: str=0) -> None:
    """Plot spectra data using the SpectraData model."""
    spectrum_data = get_spectrum_data(machine, point, proc_mode, timestamp)
    spectra = SpectraData.parse_obj(spectrum_data)
    spectra.plot()

# Helper functions
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
                      timestamp: str, type: str, output_dir: Path) -> None:
    """Save JSON data to a specified file path."""
    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to JSON file
    filename = f"{type}_{machine}_{point}_{proc_mode}_{timestamp}.json"
    filepath = f"{output_dir}/{filename}"
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)