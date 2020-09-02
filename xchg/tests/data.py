'''Test data.'''

import pandas as pd
from pytest import fixture
from ..xchg import Xchg


@fixture
def files() -> dict:
    '''A dictionary with csv files content.'''
    return {
            'cur0.csv': 'date,high,low,open,close\n'
                        '1575158400,0.02009497,0.020021,0.02007299,0.02008\n'
                        '1575160200,0.02014813,0.02007299,0.02008427,0.020124',
            'cur1.csv': 'date,high,low,open,close\n'
                        '1575158400,0.12009497,0.120021,0.12007299,0.12008\n'
                        '1575160200,0.12014813,0.12007299,0.12008427,0.120124',
            'cur2.csv': 'date,high,low,open,close\n'
                        '1575158400,0.22009497,0.220021,0.22007299,0.22008\n'
                        '1575160200,0.22014813,0.22007299,0.22008427,0.220124'
           }


@fixture
def candles() -> list:
    '''Candles which have been read from csv files.'''
    return [{
             'cur0': {'date': 1575158400,
                      'high': 0.02009497,
                      'low': 0.020021,
                      'open': 0.02007299,
                      'close': 0.02008},
             'cur1': {'date': 1575158400,
                      'high': 0.12009497,
                      'low': 0.120021,
                      'open': 0.12007299,
                      'close': 0.12008},
             'cur2': {'date': 1575158400,
                      'high': 0.22009497,
                      'low': 0.220021,
                      'open': 0.22007299,
                      'close': 0.22008}
            },
            {
             'cur0': {'date': 1575160200,
                      'high': 0.02014813,
                      'low': 0.02007299,
                      'open': 0.02008427,
                      'close': 0.020124},
             'cur1': {'date': 1575160200,
                      'high': 0.12014813,
                      'low': 0.12007299,
                      'open': 0.12008427,
                      'close': 0.120124},
             'cur2': {'date': 1575160200,
                      'high': 0.22014813,
                      'low': 0.22007299,
                      'open': 0.22008427,
                      'close': 0.220124}
            }]


@fixture
def downloaded_candles() -> list:
    '''Two candles which are downloaded from Poloniex.'''
    return [
               {
                   'date': 1575158400,
                   'high': 0.02009497,
                   'low': 0.020021,
                   'open': 0.02007299,
                   'close': 0.02008,
                   'volume': 2.83754783,
                   'quoteVolume': 141.51364588,
                   'weightedAverage': 0.0200514
               },
               {
                   'date': 1575160200,
                   'high': 0.02014813,
                   'low': 0.02007299,
                   'open': 0.02008427,
                   'close': 0.02012469,
                   'volume': 0.15556988,
                   'quoteVolume': 7.73633777,
                   'weightedAverage': 0.02010898
               }
           ]


@fixture
def dataframe() -> pd.core.frame.DataFrame:
    '''Two candles in the DataFrame.'''
    candles = list([
        [
            1575158400,
            0.02009497,
            0.020021,
            0.02007299,
            0.02008,
            2.83754783,
            141.51364588,
            0.0200514
        ],
        [
            1575160200,
            0.02014813,
            0.02007299,
            0.02008427,
            0.02012469,
            0.15556988,
            7.73633777,
            0.02010898
        ]
    ])
    columns = list([
        'date',
        'high',
        'low',
        'open',
        'close',
        'volume',
        'quoteVolume',
        'weightedAverage'
    ])
    return pd.DataFrame(candles, columns=columns)


@fixture
def balance() -> dict:
    '''A sample balance.'''
    return {'cash': 1.0, 'cur0': 0.1, 'cur1': 0.5, 'cur2': 0.0}


@fixture
def portfolio() -> dict:
    '''A test portfolio based on the sample balance.'''
    return {'cash': 0.9415770285335502,
            'cur0': 0.001890686673295369,
            'cur1': 0.05653228479315436,
            'cur2': 0.0}


@fixture
def x(candles: list, balance: dict) -> Xchg:
    '''A test Xchg object.

    Args:
        candles: A candles list.
        balance: An initial balance.
    '''
    return Xchg(balance, 0.1, 0.01, candles=candles)


@fixture
def balance_after_buy() -> dict:
    '''A balance after a buy operation.'''
    return {'cash': 0.7768888888888889, 'cur0': 10.1, 'cur1': 0.5, 'cur2': 0.0}


@fixture
def balance_after_sell() -> dict:
    '''A balance after a sell operation.'''
    return {'cash': 1.0324216, 'cur0': 0.1, 'cur1': 0.2, 'cur2': 0.0}


@fixture
def balance_after_full_buy() -> dict:
    '''A balance after buying currency for all cash.'''
    return {'cash': 0.0, 'cur0': 44.920717131474105, 'cur1': 0.5, 'cur2': 0.0}


@fixture
def balance_after_full_sell() -> dict:
    '''A balance after a complete sell of one currency.'''
    return {'cash': 1.054036, 'cur0': 0.1, 'cur1': 0.0, 'cur2': 0.0}


@fixture
def target_portfolios() -> dict:
    '''Several test cases for a desired portfolio.'''
    return [{'cash': 0.0, 'cur0': 0.2, 'cur1': 0.0, 'cur2': 0.8},
            {'cash': 0.0, 'cur0': 0.7, 'cur1': 0.3, 'cur2': 0.0},
            {'cash': 1.0, 'cur0': 0.0, 'cur1': 0.0, 'cur2': 0.0},
            {'cash': 0.2, 'cur0': 0.2, 'cur1': 0.2, 'cur2': 0.4},
            {'cash': 0.1, 'cur0': 0.9, 'cur1': 0.0, 'cur2': 0.0}]


@fixture
def xchg_repr() -> str:
    '''A representation __repr__ of Xchg class.'''
    return ("balance: {'cash': 1.0, 'cur0': 0.1, 'cur1': 0.5, 'cur2': 0.0}\n"
            "fee: 0.1\n"
            "min_order_size: 0.01\n"
            "currencies: ['cur0', 'cur1', 'cur2']\n"
            "current_candle: {"
            "'cur0': {"
            "'date': 1575158400.0, "
            "'high': 0.02009497, "
            "'low': 0.020021, "
            "'open': 0.02007299, "
            "'close': 0.02008"
            "}, "
            "'cur1': {"
            "'date': 1575158400.0, "
            "'high': 0.12009497, "
            "'low': 0.120021, "
            "'open': 0.12007299, "
            "'close': 0.12008"
            "}, "
            "'cur2': {"
            "'date': 1575158400.0, "
            "'high': 0.22009497, "
            "'low': 0.220021, "
            "'open': 0.22007299, "
            "'close': 0.22008"
            "}"
            "}\n"
            "capital: 1.062048\n"
            "portfolio: {"
            "'cash': 0.9415770285335502, "
            "'cur0': 0.001890686673295369, "
            "'cur1': 0.05653228479315436, "
            "'cur2': 0.0"
            "}")
