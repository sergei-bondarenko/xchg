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
    def balance(self) -> float:
        '''Get a current balance.

        Returns:
            A current balance.
        '''
        return self.__balance

    @property
    def fee(self) -> float:
        '''Get a fee which is used in the exchange.

        Returns:
            A fee.
        '''
        return self.__fee

    @property
    def currencies(self) -> float:
        '''Get currencies which are used in the exchange.

        Returns:
            List of currencies.
        '''
        return self.__currencies

    @property
    def min_order_size(self) -> float:
        '''Get a minimum order size which is set in the exchange.

        Returns:
            A minimum order value expressed in a cash currency.
        '''
        return self.__min_order_size

    @property
    def capital(self) -> float:
        '''Returns a current capital - sum of all currencies if they are
        converted to a cash without fees.

        Returns:
            A capital.
        '''
        capital = 0
        for currency, amount in self.balance.items():
            if currency == 'cash':
                capital += amount
            else:
                capital += amount * self.current_candle[currency]['close']
        return capital

    @property
    def portfolio(self) -> dict:
        '''Returns a current portfolio - proportion of capital by each
        currency.

        Returns:
            A portfolio.
        '''
        cap = self.capital
        portf = {}
        for currency, amount in self.balance.items():
            if currency == 'cash':
                portf[currency] = self.balance[currency] / cap
            else:
                portf[currency] = (self.balance[currency]
                                   * self.current_candle[currency]['close']
                                   / cap)
        return portf

    def next_step(self) -> 'Xchg':
        '''Go to the next step in timeline.

        Returns:
            A new Xchg instance with one candle removed.
        '''
        if len(self.__candles) == 1:
            raise StopIteration
        return Xchg(self.balance, self.fee, self.min_order_size,
                    candles=self.__candles[1:])

    def buy(self, currency: str, amount: float) -> dict:
        '''Buy currency.

        Args:
            currency: A name of the currency.
            amount: How much units of this currency to buy.

        Returns:
            A new Xchg instance after a buy operation.
        '''

        balance = self.balance.copy()
        price = self.current_candle[currency]['close']
        without_fee = price * amount
        with_fee = without_fee * (1 + self.fee)

        if (with_fee <= self.balance['cash']
                and without_fee >= self.min_order_size):
            balance['cash'] -= with_fee
            balance[currency] += amount

        return Xchg(balance, self.fee, self.min_order_size,
                    candles=self.__candles)

    def sell(self, currency: str, amount: float) -> dict:
        '''Sell currency.

        Args:
            currency: A name of the currency.
            amount: How much units of this currency to sell.

        Returns:
            A new Xchg instance after a sell operation.
        '''

        balance = self.balance.copy()
        price = self.current_candle[currency]['close']
        without_fee = price * amount
        with_fee = without_fee * (1 - self.fee)

        if (amount <= self.balance[currency]
                and without_fee >= self.min_order_size):
            balance['cash'] += with_fee
            balance[currency] -= amount

        return Xchg(balance, self.fee, self.min_order_size,
                    candles=self.__candles)
