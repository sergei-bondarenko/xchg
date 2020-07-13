'''Unit tests for xchg.py.'''

import pandas as pd
from xchg.main import _read_market
from xchg.main import next_step


def test_read_market(csv_market: tuple, tmp_path: str,
                     dataframe_market: pd.core.frame.DataFrame):
    '''Test reading csv files into a multi-index Pandas DataFrame.

    Args:
        csv_market: Test market data for several currencies in a csv form.
        tmp_path: Path which authomatically created by pytest for testing.
        dataframe_market: Test market data in a multi-index Pandas DataFrame
            form.
    '''
    for currency, candles in enumerate(csv_market):
        filepath = tmp_path / f"cur{currency}.csv"
        with open(filepath, 'w') as f:
            f.write(candles)
    pd.testing.assert_frame_equal(
        _read_market(tmp_path), dataframe_market)


def test_next_step(csv_market: tuple, tmp_path: str,
                   dataframe_market2: pd.core.frame.DataFrame):
    '''Test function for emission of next candles.

    Args:
        csv_market: Test market data for several currencies in a csv form.
        tmp_path: Path which authomatically created by pytest for testing.
        dataframe_market2: Test market data in a multi-index Pandas DataFrame
            form.
    '''
    for currency, candles in enumerate(csv_market):
        filepath = tmp_path / f"cur{currency}.csv"
        with open(filepath, 'w') as f:
            f.write(candles)
    candles = []
    for candle in next_step(tmp_path):
        candles.append(candle)
    pd.testing.assert_frame_equal(
        pd.DataFrame(candles), dataframe_market2)
