import unittest
from xchg import download_sample

class TestSum(unittest.TestCase):
  def test_request(self):
    '''Test request to Poloniex.'''
    candles = download_sample.request('ETH', 1800, 1575158400, 1575160200)
    self.assertEqual(candles,
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

if __name__ == '__main__':
  unittest.main()
