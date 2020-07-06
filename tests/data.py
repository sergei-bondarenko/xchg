'''Test data.'''

import pandas as pd
from pytest import fixture


@fixture
def test_candles() -> list:
    '''Two test candles.'''
    return list(
        [
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
    )


@fixture
def test_dataframe() -> pd.core.frame.DataFrame:
    '''Two test candles in the DataFrame.'''
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
    return pd.DataFrame(candles, columns=columns).set_index('date')


@fixture
def csv_content() -> str:
    '''Two testing candles in a CSV string.'''
    return ('date,high,low,open,close,volume,quoteVolume,weightedAverage\n'
            + '1575158400,0.02009497,0.020021,0.02007299,0.02008,2.83754783,'
            + '141.51364588,0.0200514\n'
            + '1575160200,0.02014813,0.02007299,0.02008427,0.02012469,'
            + '0.15556988,7.73633777,0.02010898\n')


@fixture
def csv_market() -> str:
    '''Three currencies market data in a csv form.'''
    return (('date,high,low,open,close\n'
            + '1575158400,0.02009497,0.020021,0.02007299,0.02008\n'
            + '1575160200,0.02014813,0.02007299,0.02008427,0.02012469'),
            ('date,high,low,open,close\n'
            + '1575158400,0.12009497,0.120021,0.12007299,0.12008\n'
            + '1575160200,0.12014813,0.12007299,0.12008427,0.12012469'),
            ('date,high,low,open,close\n'
            + '1575158400,0.22009497,0.220021,0.22007299,0.22008\n'
            + '1575160200,0.22014813,0.22007299,0.22008427,0.22012469'))


@fixture
def dataframe_market() -> pd.core.frame.DataFrame:
    '''Three currencies market data in a multi-index Pandas DataFrame form.'''
    d = {
        'currency': ['cur0', 'cur0', 'cur1', 'cur1', 'cur2', 'cur2'],
        'date': [1575158400, 1575160200, 1575158400, 1575160200, 1575158400,
                 1575160200],
        'high': [0.02009497, 0.02014813, 0.12009497, 0.12014813, 0.22009497,
                 0.22014813],
        'low': [0.020021, 0.02007299, 0.120021, 0.12007299, 0.220021,
                0.22007299],
        'open': [0.02007299, 0.02008427, 0.12007299, 0.12008427, 0.22007299,
                 0.22008427],
        'close': [0.02008, 0.02012469, 0.12008, 0.12012469, 0.22008,
                  0.22012469]
    }
    return pd.DataFrame(data=d).set_index(['currency', 'date'])
