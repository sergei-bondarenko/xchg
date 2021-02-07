'''Unit tests for xchg.py.'''

from pytest import raises
from pytest import approx
from ..xchg import Xchg


def test_init(files: dict, tmp_path: str, candles: list, balance: dict,
              xchg_repr: str, default_balance: dict):
    '''Test a construction of a Xchg class.

    Args:
        files: A dictionary with csv files content.
        tmp_path: A path which authomatically created by pytest for testing.
        candles: An expected result.
        balance: An initial balance.
        xchg_repr: A representation __repr__ of Xchg class.
        default_balance: A default balance when it is not set.
    '''
    # Prepare files.
    for filename, content in files.items():
        filepath = tmp_path / filename
        with open(filepath, 'w') as f:
            f.write(content)

    fee = 0.1
    min_order_size = 0.01
    x = Xchg(fee, min_order_size, balance=balance, data_path=tmp_path)
    assert x.current_candle == candles[0]
    assert x.balance == balance
    assert x.fee == fee
    assert x.min_order_size == min_order_size
    assert x.currencies == [f.split('.')[0] for f in files.keys()]
    assert repr(x) == xchg_repr
    x = Xchg(fee, min_order_size, tmp_path)
    assert x.balance == default_balance
    x = Xchg(fee, min_order_size, tmp_path, 1.0)
    assert x.balance == default_balance


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
    assert x.portfolio == approx(portfolio, 1e-10)


def test_buy(x: Xchg, balance_after_buy: dict, balance_after_full_buy: dict):
    '''Test a buy operation.

    Args:
        x: A Xchg instance.
        balance_after_buy: A balance after a buy operation.
        balance_after_full_buy: A balance after buying currency for all cash.
    '''
    # A normal path.
    assert x.buy('cur0', 10).balance == approx(balance_after_buy, 1e-10)

    # Buy less than a minimum order size.
    assert x.buy('cur0', 0.1).balance == approx(x.balance, 1e-10)

    # Buy more than the existing cash amount.
    assert x.buy('cur0', 100).balance == approx(x.balance, 1e-10)

    # Buy zero amount.
    assert x.buy('cur0', 0).balance == approx(x.balance, 1e-10)

    # Buy a currency for all cash.
    assert x.buy('cur0', 44.820717131474105).balance == \
           approx(balance_after_full_buy, 1e-10)

    # Buy a little more than we have cash, it must be forgived.
    assert x.buy('cur0', 44.820717131474105 + 1e-10).balance == \
           approx(balance_after_full_buy, 1e-10)


def test_sell(x: Xchg, balance_after_sell: dict,
              balance_after_full_sell: dict):
    '''Test a sell operation.

    Args:
        x: A Xchg instance.
        balance_after_sell: A balance after a sell operation.
        balance_after_full_sell: A balance after a complete sell of one
            currency.
    '''
    # A normal path.
    assert x.sell('cur1', 0.3).balance == approx(balance_after_sell, 1e-10)

    # Buy less than a minimum order size.
    assert x.sell('cur1', 0.05).balance == approx(x.balance, 1e-10)

    # Sell more than we have.
    assert x.sell('cur1', 1).balance == approx(x.balance, 1e-10)

    # Sell zero amount.
    assert x.sell('cur1', 0).balance == approx(x.balance, 1e-10)

    # Sell one currency completely.
    assert x.sell('cur1', 0.5).balance == \
           approx(balance_after_full_sell, 1e-10)

    # Sell a little more than we have, it must be forgived.
    assert x.sell('cur1', 0.5 + 1e-10).balance == \
           approx(balance_after_full_sell, 1e-10)


def test_make_portfolio(x: Xchg, target_portfolios: dict):
    '''Test a making portfolio.

    Args:
        x: A Xchg instance.
        target_portfolios: Several test cases for a desired portfolio.
    '''
    x_new = x
    for target_portfolio in target_portfolios:
        x_new = x_new.make_portfolio(target_portfolio)
        assert x_new.portfolio == approx(target_portfolio, 1e-10)
