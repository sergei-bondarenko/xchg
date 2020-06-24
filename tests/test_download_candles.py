import os
import pytest
import pandas as pd
from xchg import download_sample


@pytest.fixture
def test_candles():
  return list(
    [
      {
        'date': 1575158400,
        'high': 0.02009497,
        'low': 0.020021,
        'open': 0.02007299,
        'close': 0.02008,
        'volume': 2.83754783,
        'quoteVolume': 141.51364588,
        'weightedAverage': 0.0200514
      },
      {
        'date': 1575160200,
        'high': 0.02014813,
        'low': 0.02007299,
        'open': 0.02008427,
        'close': 0.02012469,
        'volume': 0.15556988,
        'quoteVolume': 7.73633777,
        'weightedAverage': 0.02010898
      }
    ]
  )


@pytest.fixture
def test_dataframe():
  return pd.DataFrame([
        [1575158400, 0.02009497, 0.020021, 0.02007299, 0.02008, 2.83754783, 141.51364588, 0.0200514],
        [1575160200, 0.02014813, 0.02007299, 0.02008427, 0.02012469, 0.15556988, 7.73633777, 0.02010898]
    ], columns=['date', 'high', 'low', 'open', 'close', 'volume', 'quoteVolume', 'weightedAverage']).set_index('date')


@pytest.fixture
def csv_file():
  return ('date,high,low,open,close,volume,quoteVolume,weightedAverage\n'
    + '1575158400,0.02009497,0.020021,0.02007299,0.02008,2.83754783,141.51364588,0.0200514\n'
    + '1575160200,0.02014813,0.02007299,0.02008427,0.02012469,0.15556988,7.73633777,0.02010898\n')


def test_request(test_candles):
  '''Test request to Poloniex.'''
  candles = download_sample.request('ETH', 1800, 1575158400, 1575160200)
  assert candles == test_candles


def test_candles_to_df(test_candles, test_dataframe):
  '''Test conversion from candles to a Pandas DataFrame.'''
  #assert download_sample.candles_to_df(test_candles) == test_dataframe
  pd.testing.assert_frame_equal(download_sample.candles_to_df(test_candles), test_dataframe)


def test_save_csv(test_dataframe, tmp_path, csv_file):
  '''Test saving a Pandas DataFrame to a csv file.'''
  filepath = tmp_path / 'test.csv'
  download_sample.save_csv(test_dataframe, filepath)
  with open(filepath, 'r') as f:
    csv = f.read()
  assert csv_file == csv

  
def test_request(test_candles):
  '''Test request to Poloniex.'''
  candles = download_sample.request('ETH', 1800, 1575158400, 1575160200)
  assert candles == test_candles


def test_main(tmp_path):
  '''Test main function.'''
  path = tmp_path / 'sample_data'
  download_sample.main(data_folder=path)
  assert set(os.listdir(path)) == {'ETH.csv', 'ETC.csv', 'XMR.csv', 'LTC.csv'}
