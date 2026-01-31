from dataclasses import dataclass

import numpy as np

from ..utils.decoding import decode_base64_signal


@dataclass
class BaseData:
    """Clase que representa los datos comunes 
    para waveform y spectra.""" #TODO: Add more description
    links: dict
    data: str
    factor: float
    path: str
    snap_t: float
    speed: float
    t: float
    unit_id: int
    
    def decode(self,dtype: np.dtype=np.int16) -> np.ndarray: 
        #TODO: Add description (@see decode_base64_signal)
        return decode_base64_signal(self.data,dtype=dtype) * self.factor
