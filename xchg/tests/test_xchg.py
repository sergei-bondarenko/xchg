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

    fee = 0.1
    min_order_size = 0.01
    x = Xchg(balance, fee, min_order_size, tmp_path)
    assert x.current_candle == candles[0]
    assert x.balance == balance
    assert x.fee == fee
    assert x.min_order_size == min_order_size
    assert x.currencies == [f.split('.')[0] for f in files.keys()]


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


def test_buy(x: Xchg, balance_after_buy: dict):
    '''Test a buy operation.

    Args:
        x: A Xchg instance.
        balance_after_buy: A balance after a buy operation.
    '''
    # A normal path.
    assert x.buy('cur0', 10).balance == balance_after_buy

    # Buy less than a minimum order size.
    assert x.buy('cur0', 0.1).balance == x.balance

    # Buy more than the existing cash amount.
    assert x.buy('cur0', 100).balance == x.balance


def test_sell(x: Xchg, balance_after_sell: dict):
    '''Test a sell operation.

    Args:
        x: A Xchg instance.
        balance_after_sell: A balance after a sell operation.
    '''
    # A normal path.
    assert x.sell('cur1', 0.3).balance == balance_after_sell

    # Buy less than a minimum order size.
    assert x.sell('cur1', 0.05).balance == x.balance

    # Sell more than we have.
    assert x.sell('cur1', 1).balance == x.balance
