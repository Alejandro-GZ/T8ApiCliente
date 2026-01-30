from dataclasses import dataclass

import numpy as np

from ..utils.plotting import plot_xy
from .basedata import BaseData


@dataclass
class SpectraData(BaseData):
    """Clase que representa los datos de espectro.""" #TODO: Add more description
    max_freq: float
    min_freq: float
    window: int
    
    def plot(self) -> None: 
        """Plot the spectra data.""" #TODO: Add more description (@see plot_xy)
        path = f"data/plots/spectra/ \
                spectrum_{self.path.replace(':', '_')}_{int(self.t)}.png"
        spec = self.decode(dtype=np.int16)
        freq = np.linspace(self.min_freq, self.max_freq, len(self.data))
        plot_xy(
            x=freq,
            y=spec,
            xlabel="Frequency",
            ylabel="Magnitude", #TODO: units? -> Config
            title=f"Spectra for path: {self.path}",
            output_path=path
        )
    
    @staticmethod
    def parse_obj(data: dict) -> "SpectraData": # De momento solo lo necesario
        """Parse a dictionary into a SpectraData object.""" 
        return SpectraData(
            links=data["_links"],
            factor=data["factor"],
            snap_t=data["snap_t"],
            speed=data["speed"],
            unit_id=data["unit_id"],
            path=data["path"],
            t=data["t"],
            max_freq=data["max_freq"],
            min_freq=data["min_freq"],
            window=data["window"],
            data=data["data"]
        )