'''Simulator of a currency exchange.'''

import pandas as pd
from os import path
from os import listdir
from .common import read_csv


def read_market(data_path: str) -> pd.core.frame.DataFrame:
    '''Read all csv files with candles inside the directory and compose
    a multi-index Pandas DataFrame.

    Args:
        data_path: Where csv files with data are stored.

    Returns multi-index Pandas DataFrame containing all candles for all
    currencies.
    '''
    market = None
    for idx, filename in enumerate(sorted(listdir(data_path))):
        df = read_csv(path.join(data_path, filename))
        df['currency'] = path.splitext(filename)[0]
        market = pd.concat([market, df])
    market = market.set_index('currency', append=True)
    market = market.reorder_levels(['currency', 'date'], axis=0)
    return market


# def next_step() -> dict:
#     '''Go to the next step in timeline, it yelds one new candle for each
#        currency.
#
#     Args:
#        market: The whole market from csv files represented as Numpy ndarray.
#
#     Returns dictionary with currencies and their prices.
#     '''
#     if step == None:
#         step = 0
#     else:
#         step += 1
#     yield market[:,step,:]
