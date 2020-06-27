'''Simulator of a currency exchange.'''

import numpy as np
from common import read_csv


def read_market(data_path: str, currencies: list) -> np.ndarray:
    '''Read csv files with candles and compose Numpy ndarray.

    Args:
      data_path: Where csv files with data are stored.
      currencies: List of currecies to use.

    Returns Numpy ndarray containing all candles for all currencies.
    '''
    market = None
    for idx, currency in enumerate(sorted(currencies)):
        df = read_csv(f"{data_path}/{currency}.csv")
        if market is None:
            market = np.empty((len(currencies), df.shape[0], df.shape[1]))
        market[idx] = df.to_numpy()
    return market
