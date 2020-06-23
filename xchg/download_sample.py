#!/usr/bin/env python3

'''This script downloads candles of selected cryptocurrencies from
poloniex.com and saves them into csv files.
'''

import os
import pandas as pd
from poloniex import Poloniex

CURRENCIES = ['ETH', 'ETC', 'XMR', 'LTC']
START = 1575158400   # December 1, 2019.
END = 1575244800     # December 2, 2019.
PERIOD = 1800        # Half-hour candles.
DATA_FOLDER = 'sample_data' # Folder where to save market data.


def request(currency, period, start, end):
  '''Get candles data from Poloniex exchange for a specified currency
  relative to BTC.

  Args:
    currency: Currency which we will request.
    period: Period for one candle in seconds.
    start: Start of range (UNIX timestamp).
    end: End of range (UNIX timestamp).

  Returns list of dictionaries, each of each represents one candle.
  '''
  polo = Poloniex()
  return polo.returnChartData(f"BTC_{currency}", period, start=start, end=end)


def write_df(df, filepath):
  '''Writes Pandas DataFrame to a csv file.

  Args:
    df: Pandas DataFrame.
    filepath: Path of the csv file.
  '''
  df.to_csv(filepath)



def main():
#  polo = Poloniex()
#  df = pd.DataFrame()
#
#  if not os.path.exists(DATA_FOLDER):
#    os.makedirs(DATA_FOLDER)
#
#  for currency in CURRENCIES:
#    candles = polo.returnChartData(f"BTC_{currency}", PERIOD, start=START, end=END)
#    df = pd.DataFrame(candles).set_index('date')
#    df.to_csv(f"{DATA_FOLDER}/{currency}.csv", index_label='date')
  print(download_candles('ETH', 1800, 1575158400, 1575244800))


if __name__ == '__main__':
  main()
