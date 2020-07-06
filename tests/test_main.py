'''Unit tests for xchg.py.'''

import pandas as pd
from xchg.main import read_market


def test_read_market(csv_market: tuple, tmp_path: str,
                     dataframe_market: pd.core.frame.DataFrame):
    '''Test reading csv files into a multi-index Pandas DataFrame.

    Args:
        csv_market: Test market data in a csv form.
        tmp_path: Path which authomatically created by pytest for testing.
        dataframe_market: Test market data in a multi-index Pandas DataFrame
            form.
    '''
    for currency, candles in enumerate(csv_market):
        filepath = tmp_path / f"cur{currency}.csv"
        with open(filepath, 'w') as f:
            f.write(candles)
    pd.testing.assert_frame_equal(
        read_market(tmp_path, ['cur0', 'cur1', 'cur2']),
        dataframe_market)
