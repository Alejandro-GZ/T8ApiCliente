import base64

import numpy as np


@staticmethod
def decode_base64_signal(data_b64: str, dtype: np.dtype = np.float32) -> np.ndarray:
        """Decodes a base64 encoded string into a NumPy array.

        This function takes a base64 encoded string and converts it into a NumPy array 
        of a specified data type. 
        It is useful for handling binary data that has been encoded for transmission 
        or storage.

            data_b64 (str): A base64 encoded string representing the data to be decoded.
            dtype (np.dtype, optional): The desired data type for the resulting 
                                        NumPy array. 
                                        Defaults to np.float32 if not specified.

            np.ndarray: A NumPy array containing the decoded data.
        """
        raw_bytes = base64.b64decode(data_b64)
        return np.frombuffer(raw_bytes, dtype=dtype)