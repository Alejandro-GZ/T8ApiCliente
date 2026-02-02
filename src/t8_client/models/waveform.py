from dataclasses import dataclass

import numpy as np
from numpy.fft import fft, fftfreq

from t8_client.models.config import Unit

from ..utils.plotting import plot_xy
from .basedata import BaseData


@dataclass
class WaveformData(BaseData):
    """
    Class representing waveform data, extending BaseData.

    This data class contains all common attributes from `BaseData` and adds 
    properties specific to waveform measurements, such as the sample rate 
    used during data acquisition.

    Attributes
    ----------
    sample_rate : int
        Sampling rate of the waveform data in Hz.
    """
    sample_rate: int
    
    def plot(self, unit:Unit) -> None: 
        """
    Plot the waveform data and save the figure as a PNG file.

    This method decodes the waveform data using `self.decode`, generates a 
    time axis based on the `sample_rate` and number of samples, and plots 
    the amplitude of the waveform using the `plot_xy` function. The resulting 
    plot is saved under the path `data/plots/waves/`.

    The filename is automatically generated from `self.path` and the current 
    time `self.t`. Labels and title are added for clarity.

    Notes
    -----
    - The y-axis label currently uses a placeholder "Amplitude"; units can 
      be configured if available.
    - See also `plot_xy` for details on plotting implementation.

    Returns
    -------
    None
    """
        path = "data/plots/waves/" + \
                f"wave{self.path.replace(':', '_')}_{int(self.t)}.png"
        signal = self.decode(dtype=np.int16)
        samples = len(signal)
        duration = samples / self.sample_rate
        t = np.linspace(0, duration, samples)
        plot_xy(
            x=t,
            y=signal,
            xlabel="Time (s)",
            ylabel=unit.property_name + "(" + unit.label + ")",
            title=f"Waveform for signal path: {self.path}",
            output_path=path
        )

    def compute_spectrum(self, fmin: float, fmax: float) \
        -> tuple[np.ndarray, np.ndarray]: #TODO: Retrieve fmin and fmax from config
        """
        Compute the frequency spectrum of a given waveform within a specified frequency
        range.

        Parameters:
        waveform: The input signal waveform.
        sample_rate: The sampling rate of the waveform in Hz.
        fmin: The minimum frequency of interest in Hz.
        fmax: The maximum frequency of interest in Hz.

        Returns:
        A tuple containing:
            - filtered_freqs: The corresponding frequencies within the
                specified range.
            - filtered_spectrum: The magnitude of the frequency spectrum within
                the specified range, with an RMS AC detector.
        """
        waveform = self.decode()
        sample_rate = self.sample_rate
        spectrum = fft(waveform) * 2 * np.sqrt(2)
        magintude = np.abs(spectrum) / len(spectrum)
        freqs = fftfreq(len(waveform), 1 / sample_rate)
        filtered_spectrum = magintude[(freqs >= fmin) & (freqs <= fmax)]
        filtered_freqs = freqs[(freqs >= fmin) & (freqs <= fmax)]
        return filtered_freqs, filtered_spectrum
    
    @staticmethod
    def parse_obj(data: dict) -> "WaveformData": # De momento solo lo necesario
        """
    Create a WaveformData instance from a dictionary.

    This static method parses the required fields from a dictionary and 
    returns a new `WaveformData` object. It assumes the dictionary contains 
    all necessary keys corresponding to the attributes of `WaveformData`.

    Parameters
    ----------
    data : dict
        Dictionary containing the data to populate the `WaveformData` object.
        Expected keys include:
        `_links`, `factor`, `snap_t`, `speed`, `unit_id`, `path`, `t`, 
        `sample_rate`, `data`.

    Returns
    -------
    WaveformData
        A new instance of `WaveformData` initialized with the values from `data`.
    """
        return WaveformData(
            links=data["_links"],
            factor=data["factor"],
            snap_t=data["snap_t"],
            speed=data["speed"],
            unit_id=data["unit_id"],
            path=data["path"],
            t=data["t"],
            sample_rate=data["sample_rate"],
            data=data["data"]
        )