'''Test data.'''

import pandas as pd
from pytest import fixture


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
