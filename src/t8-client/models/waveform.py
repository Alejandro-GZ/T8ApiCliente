from dataclasses import dataclass

import numpy as np
from basedata import BaseData

from ..utils.plotting import plot_xy


@dataclass
class WaveformData(BaseData):
    """Clase que representa los datos de forma de onda.""" #TODO: Add more description
    sample_rate: int
    
    def plot(self, output_path: str) -> None: #TODO: Add description (@see plot_xy)
        signal = self.decode()
        t = np.arange(len(signal)) / self.sample_rate \
            + self.timestamp # TODO: Check if OK
        plot_xy(
            x=t,
            y=signal,
            xlabel="Time [s]",
            ylabel="Amplitude", #TODO: units? -> Config
            title=f"Waveform for signal path: {self.path}",
            output_path=output_path
        )
    
    #TODO: Calc spectra