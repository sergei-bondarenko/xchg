'''Simulator of a currency exchange.'''

import numpy as np
import pandas as pd
from os import path
from os import listdir
from .common import _read_csv


def _read_market(data_path: str) -> pd.core.frame.DataFrame:
    '''Read all csv files with candles inside the directory and compose
    a Pandas DataFrame.

    Args:
        data_path: Where csv files with data are stored.

    Returns:
        A Pandas DataFrame containing all candles for all
            currencies.
    '''
    market = None
    for idx, filename in enumerate(sorted(listdir(data_path))):
        df = _read_csv(path.join(data_path, filename))
        df['currency'] = path.splitext(filename)[0]
        market = pd.concat([market, df])
    return market


def _dict_to_array(dic: dict) -> np.ndarray:
    '''Convert a dictionary to Numpy ndarray.

    Args:
        dic: A dictionary (e.g. balance, portfolio, etc.).

    Returns:
        A Numpy ndarray.
    '''
    return np.array([dic[i] for i in sorted(dic)])


def _array_to_dict(arr: np.ndarray, currencies: tuple) -> dict:
    '''Convert a Numpy ndarray to a dictionary (e.g. balance, portfolio,
    etc.).

    Args:
        arr: A Numpy ndarray.
        currencies: A tuple of currencies.

    Returns:
        A dictionary.
    '''
    return dict(zip(sorted(currencies), arr))


def _candles_to_array(candles: dict) -> np.ndarray:
    '''Convert candle close prices to a dictionary.

    Args:
        candles: A candles dictionary.

    Returns:
        A Numpy ndarray.
    '''
    # Get close prices from all currencies and prepend 1.0 as a cash price.
    prices = [candles[currency]['close'] for currency in sorted(candles)]
    return np.array([1.0] + prices)


def next_step(data_path: str) -> dict:
    '''Go to the next step in timeline, it yelds a one new candle for each
    currency.

    Args:
        data_path: Where csv files with data are stored.

    Returns:
        A dictionary with currencies and their prices.
    '''
    market = _read_market(data_path)
    for step in market.index.unique():
        yield market.loc[step].set_index('currency').to_dict('index')


def capital(candles: dict, balance: dict) -> float:
    '''Returns current capital - sum of all currencies converted to cash
    (without fees).

    Args:
        candles: Current candles as result of next_step function.
        balance: Dictionary of currencies and values representing a current
            balance.

    Returns:
        A capital.
    '''
    capital = 0
    for currency, amount in balance.items():
        if currency == 'cash':
            capital += amount
        else:
            capital += amount * candles[currency]['close']
    return capital


def portfolio(candles: dict, balance: dict) -> dict:
    '''Returns current portfolio - proportion of capital by each currency.

    Args:
        candles: Current candles as result of next_step function.
        balance: Dictionary of currencies and values representing a current
            balance.

    Returns:
        A portfolio.
    '''
    cap = capital(candles, balance)
    portfolio = {}
    for currency, amount in balance.items():
        if currency == 'cash':
            portfolio[currency] = balance[currency] / cap
        else:
            portfolio[currency] = (balance[currency]
                                   * candles[currency]['close'] / cap)
    return portfolio


def buy(candles: dict, balance: dict, currency: str, amount: float,
        fee: float, min_order_size: float) -> dict:
    '''Buy currency.

    Args:
        candles: Current candles.
        balance: Dictionary of currencies and values representing a current
            balance.
        currency: Name of the currency.
        amount: How much units of this currency to buy.
        fee: What part of the trade volume will be paid as fee.
        min_order_size: Minimum trade volume expressed in a base currency
            (cash).

    Returns:
        A new balance after trade.
    '''

    result = balance.copy()
    price = candles[currency]['close']
    without_fee = price * amount
    with_fee = without_fee * (1 + fee)

    if with_fee <= balance['cash'] and without_fee >= min_order_size:
        result['cash'] -= with_fee
        result[currency] += amount

    return result


def sell(candles: dict, balance: dict, currency: str, amount: float,
         fee: float, min_order_size: float) -> dict:
    '''Sell currency.

    Args:
        candles: Current candles.
        balance: Dictionary of currencies and values representing a current
            balance.
        currency: Name of the currency.
        amount: How much units of this currency to sell.
        fee: What part of the trade volume will be paid as fee.
        min_order_size: Minimum trade volume expressed in a base currency
            (cash).

    Returns:
        A new balance after trade.
    '''

    result = balance.copy()
    price = candles[currency]['close']
    without_fee = price * amount
    with_fee = without_fee * (1 - fee)

    if amount <= balance[currency] and without_fee >= min_order_size:
        result['cash'] += with_fee
        result[currency] -= amount

    return result


def make_portfolio(candles: dict, balance: dict, fee: float,
                   target_portfolio: dict) -> dict:
    '''Provide an answer how to make a desired portfolio.

    Args:
        candles: Current candles.
        balance: Dictionary of currencies and values representing a current
            balance.
        fee: What part of the trade volume will be paid as fee.
        target_portfolio: A desired portfolio.

    Returns:
        A dictionary with values of how much of each currency to buy
            (positive number) or sell (negative) in order to achieve a
            desired portfolio.
    '''

    prices = _candles_to_array(candles)
    cur_balance = _dict_to_array(balance)
    cur_capital = capital(candles, balance)
    cur_portfolio = cur_balance * prices / np.sum(cur_balance * prices)
    tar_portfolio = _dict_to_array(target_portfolio.copy())

    # Calculate a capital change after trading.
    cc0 = 1
    cc1 = 1 - 2 * fee + fee ** 2
    while abs(cc1 - cc0) > 1e-10:
        cc0 = cc1
        cc1 = (1 - fee * cur_portfolio[0] - (2 * fee - fee ** 2)
               * np.sum(np.maximum(cur_portfolio[1:]
                        - cc1 * tar_portfolio[1:], 0))) \
            / (1 - fee * tar_portfolio[0])

    # A capital after trade.
    tar_capital = cur_capital * cc1

    tar_balance = tar_capital * tar_portfolio / prices

    return _array_to_dict(tar_balance - cur_balance, balance.keys())
