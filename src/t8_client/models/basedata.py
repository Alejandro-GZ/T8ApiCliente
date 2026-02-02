from dataclasses import dataclass

import numpy as np

from ..utils.decoding import decode_base64_signal


@dataclass
class BaseData:
    """
    Class representing common data for waveforms and spectra.

    This data class stores the essential attributes shared by waveform and 
    spectral data, including metadata, the encoded data, scaling factor, 
    timing information, and identifiers.

    Attributes
    ----------
    links : dict
        Dictionary containing related resource links or references.
    data : str
        Base64-encoded string representing the raw data.
    factor : float
        Scaling factor to apply to the decoded data.
    path : str
        File or resource path associated with the data.
    snap_t : float
        Snapshot time or timestamp of the measurement.
    speed : float
        Speed parameter relevant to the data acquisition.
    t : float
        Time variable associated with the data.
    unit_id : int
        Identifier for the unit or measurement source.
    """
    links: dict
    data: str
    factor: float
    path: str
    snap_t: float
    speed: float
    t: float
    unit_id: int
    
    def decode(self,dtype: np.dtype=np.int16) -> np.ndarray: 
        """
    Decode Base64-encoded data and apply a scaling factor.

    This method decodes the data stored in `self.data` from Base64 using 
    the `decode_base64_signal` function, converts it to the specified 
    `dtype`, and multiplies the result by `self.factor`.

    Parameters
    ----------
    dtype : np.dtype, optional
        Data type for the resulting array. Default is `np.int16`.

    Returns
    -------
    np.ndarray
        NumPy array containing the decoded and scaled data.

    See Also
    --------
    decode_base64_signal : Function used to decode the Base64 signal.
    """
        return decode_base64_signal(self.data,dtype=dtype) * self.factor
