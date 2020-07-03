'''Unit tests for xchg.py.'''

import numpy as np
from xchg.xchg import read_market


def test_read_market(csv_market: tuple, ndarray_market: np.ndarray,
                     tmp_path: str):
    '''Test reading csv files into Numpy ndarray.

    Args:
        csv_market: Market data in a csv form.
        ndarray_market: Market data in a Numpy ndarray form.
        tmp_path: Path which authomatically created by pytest for testing.
    '''
    for currency, candles in enumerate(csv_market):
        filepath = tmp_path / f"{currency}.csv"
        with open(filepath, 'w') as f:
            f.write(candles)
    print(read_market(tmp_path, ['0', '1', '2']) - ndarray_market)
    np.testing.assert_allclose(read_market(tmp_path, ['0', '1', '2']),
                               ndarray_market, rtol=1e-15)
