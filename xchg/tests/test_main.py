'''Unit tests for xchg.py.'''

import pandas as pd
from xchg.main import _read_market
from xchg.main import next_step
from xchg.main import capital
from xchg.main import portfolio


def test_read_market(test_csv_market: tuple, tmp_path: str,
                     test_dataframe_market: pd.core.frame.DataFrame):
    '''Test reading csv files into a multi-index Pandas DataFrame.

    Args:
        test_csv_market: Test market data for several currencies in a csv form.
        tmp_path: Path which authomatically created by pytest for testing.
        test_dataframe_market: Test market data in a multi-index Pandas
            DataFrame form.
    '''
    for currency, candles in enumerate(test_csv_market):
        filepath = tmp_path / f"cur{currency}.csv"
        with open(filepath, 'w') as f:
            f.write(candles)
    pd.testing.assert_frame_equal(
        _read_market(tmp_path), test_dataframe_market)


def test_next_step(test_csv_market: tuple, tmp_path: str,
                   test_dataframe_market2: pd.core.frame.DataFrame):
    '''Test function for emission of next candles.

    Args:
        test_csv_market: Test market data for several currencies in a csv form.
        tmp_path: Path which authomatically created by pytest for testing.
        test_dataframe_market2: Test market data in a multi-index Pandas
            DataFrame form.
    '''
    for currency, candles in enumerate(test_csv_market):
        filepath = tmp_path / f"cur{currency}.csv"
        with open(filepath, 'w') as f:
            f.write(candles)
    candles = []
    for candle in next_step(tmp_path):
        candles.append(candle)
    pd.testing.assert_frame_equal(
        pd.DataFrame(candles), test_dataframe_market2)


def test_capital(test_dataframe_market2: pd.core.frame.DataFrame,
                 test_balance: dict, test_capital: float):
    '''Test capital function.

    Args:
        test_dataframe_market2: Test market data in a multi-index Pandas
            DataFrame form.
        test_balance: Test balance dictionary.
        test_capital: Test result of capital function.
    '''
    candles = test_dataframe_market2.loc[0].to_dict()
    assert capital(candles, test_balance) == test_capital


def test_portfolio(test_dataframe_market2: pd.core.frame.DataFrame,
                   test_balance: dict, test_portfolio: dict):
    '''Test capital function.

    Args:
        test_dataframe_market2: Test market data in a multi-index Pandas
            DataFrame form.
        test_balance: Test balance dictionary.
        test_portfolio: Test result of portfolio function.
    '''
    candles = test_dataframe_market2.loc[0].to_dict()
    assert portfolio(candles, test_balance) == test_portfolio
