import os
import pytest
import pandas as pd
from xchg import download_sample


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


def test_candles_to_df(test_candles: list,
                       test_dataframe: pd.core.frame.DataFrame):
    '''Test conversion from candles to a Pandas DataFrame.'''
    downloaded_df = download_sample.candles_to_df(test_candles)
    pd.testing.assert_frame_equal(downloaded_df, test_dataframe)


def test_save_csv(test_dataframe: pd.core.frame.DataFrame,
                  tmp_path: str, csv_file: str):
    '''Test saving a Pandas DataFrame to a csv file.'''
    filepath = tmp_path / 'test.csv'
    download_sample.save_csv(test_dataframe, filepath)
    with open(filepath, 'r') as f:
        csv = f.read()
    assert csv_file == csv


def test_request(test_candles: list):
    '''Test request to Poloniex.'''
    candles = download_sample.request('ETH', 1800, 1575158400, 1575160200)
    assert candles == test_candles


def test_main(tmp_path: str):
    '''Test main function.'''
    path = tmp_path / 'sample_data'
    download_sample.main(data_folder=path)
    currencies = {'ETH.csv', 'ETC.csv', 'XMR.csv', 'LTC.csv'}
    assert set(os.listdir(path)) == currencies
