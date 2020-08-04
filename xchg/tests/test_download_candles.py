'''Unit tests for download_candles.py.'''

import os
import pandas as pd
from xchg.download_sample import _request
from xchg.download_sample import _candles_to_df
from xchg.download_sample import _main


def test_candles_to_df(test_list_candles: list,
                       test_pandas_dataframe: pd.core.frame.DataFrame):
    '''Test conversion from candles to a Pandas DataFrame.

    Args:
        test_list_candles: Test candles in a list.
        test_pandas_dataframe: Pandas DataFrame with test candles.
    '''
    downloaded_df = _candles_to_df(test_list_candles)
    pd.testing.assert_frame_equal(downloaded_df, test_pandas_dataframe,
                                  check_exact=True)


def test_request(test_list_candles: list):
    '''Test request to Poloniex.

    Args:
        test_list_candles: Test candles in a list.
    '''
    candles = _request('ETH', 1800, 1575158400, 1575160200)
    assert candles == test_list_candles


def test_main(tmp_path: str):
    '''Test main function.

    Args:
        tmp_path: Path which authomatically created by pytest for testing.
    '''
    path = tmp_path / 'sample_data'
    _main(data_folder=path)
    currencies = {'ETH.csv', 'ETC.csv', 'XMR.csv', 'LTC.csv'}
    assert set(os.listdir(path)) == currencies
