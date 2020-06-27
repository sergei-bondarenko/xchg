'''Unit tests for common.py.'''

import pandas as pd
from xchg.common import save_csv


def test_save_csv(test_dataframe: pd.core.frame.DataFrame,
                  tmp_path: str, csv_file: str):
    '''Test saving a Pandas DataFrame to a csv file.'''
    filepath = tmp_path / 'test.csv'
    save_csv(test_dataframe, filepath)
    with open(filepath, 'r') as f:
        csv = f.read()
    assert csv_file == csv
