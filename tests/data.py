'''Test data.'''

import pytest
import pandas as pd


@pytest.fixture
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


@pytest.fixture
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


@pytest.fixture
def csv_file() -> str:
    '''Two testing candles in csv string.'''
    return ('date,high,low,open,close,volume,quoteVolume,weightedAverage\n'
            + '1575158400,0.02009497,0.020021,0.02007299,0.02008,2.83754783,'
            + '141.51364588,0.0200514\n'
            + '1575160200,0.02014813,0.02007299,0.02008427,0.02012469,'
            + '0.15556988,7.73633777,0.02010898\n')
