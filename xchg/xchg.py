'''Simulator of a currency exchange.'''

from .common import _read_candles


class Xchg:
    def __init__(self, fee, min_order_size, data_path=None, balance=None,
                 candles=None):
        '''Create an instance of a currency exchange.

        Args:
          fee: What part of a trade volume will be paid as fee. For example, 1%
              fee should be set as 0.01.
          min_order_size: Minimum trade volume expressed in a base currency
              (cash).
          data_path: Where csv files with data are stored.
          balance: An initial balance. If it's None, then cash currency will be
              set to 1.0 and all others to zero. If it's a float, then it will
              set as the base currency (cash) value. Also you set it as a full
              dictionary with all currencies as keys and values.
          candles: You can directly initialize the class with candles, not to
              read them from a disk.
        '''
        self.__fee = fee
        self.__min_order_size = min_order_size

        if data_path is not None:
            res = _read_candles(data_path)
            self.__currencies = res['currencies']
            self.__candles = res['candles']
        else:
            self.__currencies = list(sorted(candles[0].keys()))
            self.__candles = candles

        self.__data_start = self.__candles[0][self.__currencies[0]]['date']
        self.__data_end = self.__candles[-1][self.__currencies[0]]['date']

        if type(balance) == dict:
            self.__balance = {}
            for currency in ['cash'] + self.__currencies:
                self.__balance[currency] = float(balance.get(currency, 0.0))
        elif balance is None:
            self.__balance = {}
            self.__balance['cash'] = 1.0
            for currency in self.__currencies:
                self.__balance[currency] = 0.0
        else:
            self.__balance = {}
            self.__balance['cash'] = float(balance)
            for currency in self.__currencies:
                self.__balance[currency] = 0.0

    def __repr__(self):
        '''Returns class attributes as a string.'''
        return (f"balance: {self.balance}\n"
                f"fee: {self.fee}\n"
                f"min_order_size: {self.min_order_size}\n"
                f"currencies: {self.currencies}\n"
                f"current_candle: {self.current_candle}\n"
                f"capital: {self.capital}\n"
                f"portfolio: {self.portfolio}\n"
                f"lenght: {len(self)}\n"
                f"data_start: {self.data_start}\n"
                f"data_end: {self.data_end}")

    def __len__(self):
        '''Returns the number of candles.'''
        return len(self.__candles)

    @property
    def data_start(self) -> int:
        '''Get a starting time of the data.

        Returns:
            A starting time of the data.
        '''
        return self.__data_start

    @property
    def data_end(self) -> int:
        '''Get an ending time of the data.

        Returns:
            An ending time of the data.
        '''
        return self.__data_end

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
        return Xchg(self.fee, self.min_order_size, balance=self.balance,
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
        currency_delta = amount * (1 - self.fee)
        cash_delta = price * amount

        # If we want to buy a slightly more than we have, we will forgive.
        if (cash_delta <= (self.balance['cash'] + 1e-10)
                and cash_delta >= self.min_order_size):
            balance['cash'] -= cash_delta
            balance[currency] += currency_delta
            if balance['cash'] < 0.0:
                # Set the balance to zero if we bought a slightly more than we
                # have.
                balance['cash'] = 0.0

        return Xchg(self.fee, self.min_order_size, balance=balance,
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

        # If we want to sell a slightly more than we have, we will forgive.
        if (amount <= (self.balance[currency] + 1e-10)
                and without_fee >= self.min_order_size):
            balance['cash'] += with_fee
            balance[currency] -= amount
            if balance[currency] < 0.0:
                # Set the balance to zero if we bought a slightly more than we
                # have.
                balance[currency] = 0.0

        return Xchg(self.fee, self.min_order_size, balance=balance,
                    candles=self.__candles)

    def make_portfolio(self, target_portfolio: dict) -> dict:
        '''Make a desired portfolio.

        Args:
            target_portfolio: A desired portfolio.

        Returns:
            A new Xchg instance with a desired portfolio distribution.
        '''

        x = self

        # Calculate a capital change after trading.
        cc0 = 1
        cc1 = 1 - 2 * x.fee + x.fee ** 2
        while abs(cc1 - cc0) > 1e-10:
            cc0 = cc1

            # How much we will get from selling.
            sell_amount = 0
            for cur in x.currencies:
                amount = x.portfolio[cur] - cc1 * target_portfolio[cur]
                if amount > 0:
                    sell_amount += amount

            cc1 = (1 - x.fee * x.portfolio['cash'] - (2 * x.fee - x.fee ** 2)
                   * sell_amount) \
                / (1 - x.fee * target_portfolio['cash'])

        # A capital after trade.
        tar_capital = x.capital * cc1

        # Sell first.
        for cur in x.currencies:
            amount = tar_capital * target_portfolio[cur] \
                     / x.current_candle[cur]['close'] - x.balance[cur]
            if amount < 0:
                x = x.sell(cur, abs(amount))

        # Then buy.
        for cur in x.currencies:
            amount = tar_capital * target_portfolio[cur] \
                     / x.current_candle[cur]['close'] - x.balance[cur]
            if amount > 0:
                x = x.buy(cur, abs(amount / (1 - self.fee)))

        return x
