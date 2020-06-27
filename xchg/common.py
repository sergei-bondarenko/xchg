'''Common functions used by several files.'''

import pandas as pd


def save_csv(df: pd.core.frame.DataFrame, filepath: str):
    '''Saves Pandas DataFrame to a csv file.

    Args:
        df: Pandas DataFrame.
        filepath: Path of the csv file.
    '''
    df.to_csv(filepath)


def read_csv(filepath: str) -> pd.core.frame.DataFrame:
    '''Read csv file into Pandas DataFrame.

    Args:
      filepath: Path to a csv file with data is stored.

    Returns Pandas DataFrame with candles.
    '''
    return pd.read_csv(filepath)
