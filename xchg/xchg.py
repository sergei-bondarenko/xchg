'''Simulator of a currency exchange.'''

from .common import _read_candles


class Xchg:
    def __init__(self, balance, fee, min_order_size, data_path=None,
                 candles=None):
        '''Create an instance of a currency exchange.

        Args:
          balance: An initial balance.
          fee: What part of a trade volume will be paid as fee.
          min_order_size: Minimum trade volume expressed in a base currency
              (cash).
          data_path: Where csv files with data are stored.
          candles: You can directly initialize the class with candles, not to
              read them from a disk.
        '''
        self.__balance = balance
        self.__fee = fee
        self.__min_order_size = min_order_size
        if data_path is not None:
            res = _read_candles(data_path)
            self.__currencies = res['currencies']
            self.__candles = res['candles']
        else:
            self.__currencies = list(sorted(candles[0].keys()))
            self.__candles = candles

    @property
    def current_candle(self) -> dict:
        '''Get a current candle.

        Returns:
            A current candle.
        '''
        return self.__candles[0]

    @property
    def capital(self) -> float:
        '''Returns a current capital - sum of all currencies if they are
        converted to a cash without fees.

        Returns:
            A capital.
        '''
        capital = 0
        for currency, amount in self.__balance.items():
            if currency == 'cash':
                capital += amount
            else:
                print('==========')
                print(currency, amount, self.current_candle[currency]['close'])
                print(capital)
                capital += amount * self.current_candle[currency]['close']
        return capital

    def next_step(self) -> 'Xchg':
        '''Go to the next step in timeline.

        Returns:
            A new Xchg instance with one candle removed.
        '''
        if len(self.__candles) == 1:
            raise StopIteration
        return Xchg(self.__balance, self.__fee, self.__min_order_size,
                    candles=self.__candles[1:])
