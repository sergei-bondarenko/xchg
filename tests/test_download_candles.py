'''Unit tests for download_candles.py.'''

import os
import pandas as pd
from xchg import download_sample


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
