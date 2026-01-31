from dataclasses import dataclass

import numpy as np
from numpy.fft import fft, fftfreq

from ..utils.plotting import plot_xy
from .basedata import BaseData


@dataclass
class WaveformData(BaseData):
    """Clase que representa los datos de forma de onda.""" #TODO: Add more description
    sample_rate: int
    
    def plot(self) -> None: #TODO: Add description (@see plot_xy)
        path = "data/plots/waves/" + \
                f"wave{self.path.replace(':', '_')}_{int(self.t)}.png"
        signal = self.decode(dtype=np.int16)
        samples = len(signal)
        duration = samples / self.sample_rate
        t = np.linspace(0, duration, samples)
        plot_xy(
            x=t,
            y=signal,
            xlabel="Time [s]",
            ylabel="Amplitude", #TODO: units? -> Config
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
        """Parse a dictionary into a WaveformData object.""" 
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