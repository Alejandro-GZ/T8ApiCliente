from unittest.mock import patch

import numpy as np

from t8_client.models.basedata import BaseData


def test_decode_applies_factor_and_dtype() -> None:
    fake_signal = np.array([1, 2, 3], dtype=np.int16)

    base = BaseData(
        links={},
        data="BASE64_FAKE",
        factor=2.0,
        path="M1:P1",
        snap_t=0,
        speed=0,
        t=0,
        unit_id=1
    )

    with patch(
        "t8_client.models.basedata.decode_base64_signal",
        return_value=fake_signal
    ) as mock_decode:

        result = base.decode(dtype=np.int16)

        mock_decode.assert_called_once_with("BASE64_FAKE", dtype=np.int16)
        assert np.array_equal(result, fake_signal * 2)

def test_decode_with_float_dtype() -> None:
    fake_signal = np.array([0.5, 1.5], dtype=np.float32)

    base = BaseData(
        links={},
        data="BASE64_FAKE",
        factor=1.0,
        path="M1:P1",
        snap_t=0,
        speed=0,
        t=0,
        unit_id=1
    )

    with patch(
        "t8_client.models.basedata.decode_base64_signal",
        return_value=fake_signal
    ) as mock_decode:

        result = base.decode(dtype=np.float32)

        mock_decode.assert_called_once_with("BASE64_FAKE", dtype=np.float32)
        assert result.dtype == np.float32
        assert np.array_equal(result, fake_signal)
        
def test_decode_zero_factor() -> None:
    fake_signal = np.array([1, -1, 2], dtype=np.int16)

    base = BaseData(
        links={},
        data="BASE64_FAKE",
        factor=0.0,
        path="M1:P1",
        snap_t=0,
        speed=0,
        t=0,
        unit_id=1
    )

    with patch(
        "t8_client.models.basedata.decode_base64_signal",
        return_value=fake_signal
    ):

        result = base.decode()

        assert np.all(result == 0)


