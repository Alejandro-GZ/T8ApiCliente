from dataclasses import dataclass

import numpy as np

from ..utils.plotting import plot_xy
from .basedata import BaseData


@dataclass
class SpectraData(BaseData):
    """
    Class representing spectral data, extending BaseData.

    This data class contains all common attributes from BaseData and adds 
    additional properties specific to spectral measurements, such as frequency 
    range and analysis window.

    Attributes
    ----------
    max_freq : float
        Maximum frequency included in the spectrum.
    min_freq : float
        Minimum frequency included in the spectrum.
    window : int
        Size of the window used for spectral analysis.
    """
    max_freq: float
    min_freq: float
    window: int
    
    def plot(self) -> None: 
        """
    Plot the spectral data and save the figure as a PNG file.

    This method decodes the spectral data using `self.decode`, generates the 
    frequency axis based on `min_freq` and `max_freq`, and plots the magnitude 
    spectrum using the `plot_xy` function. The resulting plot is saved to a 
    file under the path `data/plots/spectra/`.

    The filename is automatically generated from `self.path` and the current 
    time `self.t`. Labels and title are added for clarity.

    Notes
    -----
    - The y-axis label currently uses a placeholder "Magnitude"; units can be 
      configured if available.
    - See also `plot_xy` for details on plotting implementation.

    Returns
    -------
    None
    """
        path = "data/plots/spectra/" + \
                f"spectrum_{self.path.replace(':', '_')}_{int(self.t)}.png"
        spec = self.decode(dtype=np.int16)
        num_bins = len(spec)
        freq = np.linspace(self.min_freq, self.max_freq, num_bins)
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
        """
    Create a SpectraData instance from a dictionary.

    This static method parses the required fields from a dictionary and 
    returns a new `SpectraData` object. It assumes the dictionary contains 
    all necessary keys corresponding to the attributes of `SpectraData`.

    Parameters
    ----------
    data : dict
        Dictionary containing the data to populate the `SpectraData` object.
        Expected keys include:
        `_links`, `factor`, `snap_t`, `speed`, `unit_id`, `path`, `t`, 
        `max_freq`, `min_freq`, `window`, `data`.

    Returns
    -------
    SpectraData
        A new instance of `SpectraData` initialized with the values from `data`.
    """
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