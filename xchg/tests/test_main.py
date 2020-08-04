'''Unit tests for xchg.py.'''

import numpy as np
import pandas as pd
from pytest import approx
from xchg.main import _read_market
from xchg.main import _dict_to_array
from xchg.main import _array_to_dict
from xchg.main import next_step
from xchg.main import capital
from xchg.main import portfolio
from xchg.main import buy
from xchg.main import sell
from xchg.main import make_portfolio


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


def test_dict_to_array(test_balance: dict, test_balance_ndarray: np.ndarray):
    '''Test conversion from a dictionary to a Numpy ndarray.

    Args:
        test_balance: A test balance dictionary.
        test_balance_ndarray: A test balance ndarray.
    '''
    arr = _dict_to_array(test_balance)
    np.testing.assert_array_equal(arr, test_balance_ndarray)


def test_array_to_dict(test_balance: dict, test_balance_ndarray: np.ndarray):
    '''Test conversion from a Numpy ndarray to a dictionary.

    Args:
        test_balance: A test balance dictionary.
        test_balance_ndarray: A test balance ndarray.
    '''
    currencies = test_balance.keys()
    dic = _array_to_dict(test_balance_ndarray, currencies)
    assert dic == test_balance


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


def test_buy(test_dataframe_market2: pd.core.frame.DataFrame,
             test_balance: dict,
             test_balance_after_buy: dict):
    '''Test buy function.

    Args:
        test_dataframe_market2: Test market data in a multi-index Pandas
            DataFrame form.
        test_balance: Test balance dictionary.
        test_balance_after_buy: Test balance after buy.
    '''
    candles = test_dataframe_market2.loc[0].to_dict()

    # Test happy path.
    assert buy(candles, test_balance, 'cur1', 3, 0.03, 0.001) \
        == approx(test_balance_after_buy)

    # Try to buy more than we have cash.
    assert buy(candles, test_balance, 'cur1', 5, 0.03, 0.001) \
        == approx(test_balance)

    # Try to buy less than minimum order size.
    assert buy(candles, test_balance, 'cur1', 3, 0.03, 10) \
        == approx(test_balance)


def test_sell(test_dataframe_market2: pd.core.frame.DataFrame,
              test_balance: dict,
              test_balance_after_sell: dict):
    '''Test sell function.

    Args:
        test_dataframe_market2: Test market data in a multi-index Pandas
            DataFrame form.
        test_balance: Test balance dictionary.
        test_balance_after_sell: Test balance after sell.
    '''
    candles = test_dataframe_market2.loc[0].to_dict()

    # Test happy path.
    assert sell(candles, test_balance, 'cur1', 0.2, 0.01, 0.001) \
        == approx(test_balance_after_sell)

    # Try to sell more than we have currency.
    assert sell(candles, test_balance, 'cur1', 0.3, 0.01, 0.001) \
        == approx(test_balance)

    # Try to sell less than minimum order size.
    assert sell(candles, test_balance, 'cur1', 0.2, 0.01, 10) \
        == approx(test_balance)


def test_make_portfolio(test_dataframe_market2: pd.core.frame.DataFrame,
                        test_balance: dict,
                        target_portfolio: dict,
                        test_balance_after_make_portfolio: dict):
    '''Test make portfolio function.

    Args:
        test_dataframe_market2: Test market data in a multi-index Pandas
            DataFrame form.
        test_balance: Test balance dictionary.
        target_portfolio: Target portfolio dictionary.
        test_balance_after_make_portfolio: Test balance after make portfolio.
    '''
    with open('/tmp/res1.txt', 'w') as f:
        f.write(f"{target_portfolio}")
    candles = test_dataframe_market2.loc[0].to_dict()
    assert test_balance_after_make_portfolio \
        == make_portfolio(candles, test_balance, 0.01, target_portfolio)
