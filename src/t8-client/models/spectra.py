from dataclasses import dataclass

from basedata import BaseData


@dataclass
class SpectraData(BaseData):
    """Clase que representa los datos de espectro.""" #TODO: Add more description
    max_freq: float
    min_freq: float
    window: int
    
    #TODO: plot spectra