'''This script downloads candles of selected cryptocurrencies from
poloniex.com and saves them into csv files.

After package installation just run "download_candles" script in your
CLI without any parameters in order to download sample data.
'''

import os
import pandas as pd
from poloniex import Poloniex
from .common import _save_csv


def _request(currency: str, period: int, start: int, end: int) -> list:
    '''Get candles data from Poloniex exchange for a specified currency
    relative to BTC.

    Args:
        currency: Currency which we will request.
        period: Period for one candle in seconds.
        start: Start of the range (UNIX timestamp).
        end: End of the range (UNIX timestamp).

    Returns:
        A list of dictionaries, each of each represents one candle.
    '''
    polo = Poloniex()
    pair = f"BTC_{currency}"
    return polo.returnChartData(pair, period, start=start, end=end)


def _candles_to_df(candles: list) -> pd.core.frame.DataFrame:
    '''Converts list of candles to a Pandas DataFrame.

    Args:
        candles: List of candles.

    Returns Pandas DataFrame filled with candles.
    '''
    return pd.DataFrame(candles, columns=[
            'date', 'high', 'low', 'open', 'close',
            'volume', 'quoteVolume', 'weightedAverage'
        ])


def _main(currencies: list = ['ETH', 'ETC', 'XMR', 'LTC'],
          start: int = 1575158400,
          end: int = 1575244800,
          period: int = 1800,
          data_folder: int = 'sample_data'):
    '''Download candles for specified currencies and range and save them
    to a separate csv files.

    Args:
        currencies: List of currencies to request from Poloniex.
        start: Starting date of the requested range (UNIX timestamp, default
            value is December 1, 2019).
        end: Ending date of the requested range (UNIX timestamp, default
            value is December 2, 2019).
        period: Period for one candle in seconds (Half-hour candles by
            default).
        data_folder: Folder where to save market data.
    '''

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    for currency in currencies:
        candles = _request(currency, period, start, end)
        df = _candles_to_df(candles)
        _save_csv(df, f"{data_folder}/{currency}.csv")

    print(f"Market data saved to {data_folder}.")
