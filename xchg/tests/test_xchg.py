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


def test_next_step(candles: list, balance: dict):
    '''Test a next_step method.

    Args:
        candles: A candles list.
        balance: An initial balance.
    '''
    x = Xchg(balance, 0, 0, candles=candles).next_step()
    assert x.current_candle == candles[1]

    # Test for an exception at the end of a file.
    with raises(StopIteration):
        x.next_step()


def test_capital(candles: list, balance: dict):
    '''Test a capital property.

    Args:
        candles: A candles list.
        balance: An initial balance.
    '''
    x = Xchg(balance, 0, 0, candles=candles)
    assert x.capital == 1.062048
