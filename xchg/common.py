'''Common functions used by several sub-modules. It's for
internal use only.'''

import pandas as pd


def _save_csv(df: pd.core.frame.DataFrame, filepath: str):
    '''Saves Pandas DataFrame to a csv file.

    Args:
        df: Pandas DataFrame.
        filepath: Path of the csv file.
    '''
    df.to_csv(filepath, index=False)


def _read_csv(filepath: str) -> pd.core.frame.DataFrame:
    '''Read csv file into Pandas DataFrame.

    Args:
      filepath: Path to a csv file with data is stored.

    Returns:
        A Pandas DataFrame with candles.
    '''
    return pd.read_csv(filepath)
