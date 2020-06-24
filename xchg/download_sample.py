#!/usr/bin/env python3

'''This script downloads candles of selected cryptocurrencies from
poloniex.com and saves them into csv files.
'''

import os
import pandas as pd
from poloniex import Poloniex


def request(currency, period, start, end):
  '''Get candles data from Poloniex exchange for a specified currency
  relative to BTC.

  Args:
    currency: Currency which we will request.
    period: Period for one candle in seconds.
    start: Start of the range (UNIX timestamp).
    end: End of the range (UNIX timestamp).

  Returns list of dictionaries, each of each represents one candle.
  '''
  polo = Poloniex()
  return polo.returnChartData(f"BTC_{currency}", period, start=start, end=end)


def candles_to_df(candles):
  '''Converts list of candles to a Pandas DataFrame.

  Args:
    candles: List of candles.

  Returns Pandas DataFrame.
  '''
  return pd.DataFrame(candles, columns=[
      'date', 'high', 'low', 'open', 'close',
      'volume', 'quoteVolume', 'weightedAverage'
    ]).set_index('date')


def save_csv(df, filepath):
  '''Saves Pandas DataFrame to a csv file.

  Args:
    df: Pandas DataFrame.
    filepath: Path of the csv file.
  '''
  df.to_csv(filepath)


def main(currencies=['ETH', 'ETC', 'XMR', 'LTC'], start=1575158400,
         end=1575244800, period=1800, data_folder='sample_data'):
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
    candles = request(currency, period, start, end)
    df = candles_to_df(candles)
    save_csv(df, f"{data_folder}/{currency}.csv")


if __name__ == '__main__':
  main()
