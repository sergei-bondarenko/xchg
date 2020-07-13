'''Unit tests for common.py.'''

import pandas as pd
from xchg.common import _save_csv
from xchg.common import _read_csv


def test_save_csv(test_dataframe: pd.core.frame.DataFrame,
                  tmp_path: str, csv_content: str):
    '''Test saving a Pandas DataFrame to a CSV file.

    Args:
        test_dataframe: Pandas DataFrame with test candles.
        tmp_path: Path which authomatically created by pytest for testing.
        csv_content_one: Expected content of a CSV file.
    '''
    filepath = tmp_path / 'test.csv'
    _save_csv(test_dataframe, filepath)
    with open(filepath, 'r') as f:
        csv = f.read()
    assert csv_content == csv


def test_read_csv(test_dataframe: pd.core.frame.DataFrame,
                  tmp_path: str, csv_content: str):
    '''Test reading of a CSV file into a Pandas DataFrame.

    Args:
        test_dataframe: Expected Pandas DataFrame with test candles.
        tmp_path: Path which authomatically created by pytest for testing.
        csv_content: Content of a CSV file.
    '''
    filepath = tmp_path / 'test.csv'
    with open(filepath, 'w') as f:
        f.write(csv_content)
    pd.testing.assert_frame_equal(_read_csv(filepath), test_dataframe,
                                  check_exact=True)
