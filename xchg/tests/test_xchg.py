'''Unit tests for xchg.py.'''

from pytest import raises
from ..xchg import Xchg


def test_init(files: dict, tmp_path: str, candles: list, balance: dict):
    '''Test a construction of a Xchg class.

    Args:
        files: A dictionary with csv files content.
        tmp_path: A path which authomatically created by pytest for testing.
        candles: An expected result.
        balance: An initial balance.
    '''
    # Prepare files.
    for filename, content in files.items():
        filepath = tmp_path / filename
        with open(filepath, 'w') as f:
            f.write(content)

    x = Xchg(balance, 0, 0, tmp_path)
    assert x.current_candle == candles[0]
    assert x.balance == balance


def test_next_step(x: Xchg, candles: list):
    '''Test a next_step method.

    Args:
        x: A Xchg instance.
        candles: A candles list.
    '''
    x = x.next_step()
    assert x.current_candle == candles[1]

    # Test for an exception at the end of a file.
    with raises(StopIteration):
        x.next_step()


def test_capital(x: Xchg):
    '''Test a capital property.

    Args:
        x: A Xchg instance.
    '''
    assert x.capital == 1.062048


def test_portfolio(x: Xchg, portfolio: dict):
    '''Test a portfolio property.

    Args:
        x: A Xchg instance.
        portfolio: A sample portfolio.
    '''
    assert x.portfolio == portfolio
