import numpy as np
import pandas as pd


class Exchange:
  def __init__(self, cash_amount, fee, min_order_size, data_path, currencies):
    '''Simulator of a currency exchange.

    Args:
      cash_amount: How much of base currency (cash) we will have.
      fee: Fee in percents for each trade.
      min_order_size: Minimum trade volume expressed in a base currency
        (cash).
      data_path: Where csv files with data are stored.
      currencies: List of currecies names to use.
    '''

    self.fee = fee
    self.min_order_size = min_order_size
    self.currencies = currencies
    self.__current_step = 0
    self.__market = dict()  # Market data.

    # Our current balance for all currencies.
    self.balance = {'cash': cash_amount}
    
    for currency in self.currencies:
      # Load data from csv file to market dictionary.
      self.__market[currency] = pd.read_csv(f"{data_path}/{currency}.csv")
      
      # Set balance for this currency as zero.
      self.balance[currency] = 0


  @property
  def current_candles(self):
    '''Returns current candles for all available currencies.'''
    candles_dict = dict()

    for currency, candles in self.__market.items():
      candles_dict[currency] = candles.iloc[self.__current_step]

    return candles_dict


  def buy(self, currency, amount):
    '''Buy currency.
    
    Args:
      currency: Name of the currency.
      amount: How much units of this currency to buy.

    Returns:
      0: Successfully bought.
      1: Not enough funds.
      2: Order is smaller than the minimum.
      3: Not enough funds and order is smaller than the minimum.
    '''

    price = self.current_candles[currency]['close']
    without_fee = price * amount
    with_fee = without_fee * (1 + self.fee / 100)

    result = 0

    if with_fee > self.balance['cash']:
      result += 1

    if without_fee < self.min_order_size:
      result += 2

    if result == 0:
      self.balance['cash'] -= with_fee
      self.balance[currency] += amount

    return result


  def sell(self, currency, amount):
    '''Sell currency.
    
    Args:
      currency: Name of the currency.
      amount: How much units of this currency to sell.

    Returns:
      0: Successfully sold.
      1: Not enough funds.
      2: Order is smaller than the minimum.
      3: Not enough funds and order is smaller than the minimum.
    '''

    price = self.current_candles[currency]['close']
    without_fee = price * amount
    with_fee = without_fee * (1 - self.fee / 100)

    result = 0

    if amount > self.balance[currency]:
      result += 1

    if without_fee < self.min_order_size:
      result += 2

    if result == 0:
      self.balance[currency] -= amount
      self.balance['cash'] += with_fee

    return result


  def next_step(self):
    '''Go to the next time period.
    
    Returns:
      0: Successfully moved to the next time period.
      1: Can't move, end of data.
    '''

    last_step = len(self.__market[self.currencies[0]]) - 1

    if self.__current_step < last_step:
      self.__current_step += 1
      result = 0
    else:
      result = 1

    return result


  def make_portfolio(self, portfolio):
    '''Buy/sell assests according a desired portfolio. Portfolio
       is a distribution of funds between currencies.

    Args:
      portfolio: Target portfolio represented as dictionary
        of currencies as keys and portions as values.

    Returns:
      0: Successfully distributed funds according requested
        portfolio.
      1: Unable to perform some trades.
    '''

    current_balance = self.balance
    candles = self.current_candles
    fee = self.fee / 100

    # Calculate current portfolio.
    current_portfolio = np.empty(len(current_balance))
    for index, (currency, amount) in enumerate(current_balance.items()):
      if currency == 'cash':
        current_portfolio[index] = amount
      else:
        current_portfolio[index] = amount * candles[currency]['close']
    current_portfolio_volume = np.sum(current_portfolio)
    current_portfolio /= current_portfolio_volume

    # Convert target portfolio from dict to numpy array.
    target_portfolio = np.empty(len(current_balance))
    for index, (currency, value) in enumerate(portfolio.items()):
      target_portfolio[index] = value

    # Calculate portfolio volume change after trading.
    pvc0 = 1
    pvc1 = 1 - 2 * fee + fee ** 2
    while abs(pvc1 - pvc0) > 1e-10:
      pvc0 = pvc1
      pvc1 = (1 - fee * current_portfolio[0]
             - (2 * fee - fee ** 2)
             * np.sum(np.maximum(current_portfolio[1:] \
             - pvc1 * target_portfolio[1:], 0))) \
             / (1 - fee * target_portfolio[0])

    target_portfolio_volume = current_portfolio_volume * pvc1

    # Calculate a target balance.
    target_balance = {}
    for index, (currency, amount) in enumerate(current_balance.items()):
      if currency == 'cash':
        target_balance[currency] = target_portfolio_volume * target_portfolio[0]
      else:
        target_balance[currency] = target_portfolio_volume * target_portfolio[index] / candles[currency]['close']

    result = 0 # Value which will be returned by this method.

    # Sell.
    for currency, amount in current_balance.items():
      if currency != 'cash':
        amount = current_balance[currency] - target_balance[currency]
        if amount > 0:
          res = self.sell(currency, amount)
          result += res

    # Buy.
    for currency, amount in current_balance.items():
      if currency != 'cash':
        amount = target_balance[currency] - current_balance[currency]
        if amount > 0:
          res = self.buy(currency, amount)
          result += res

    if result > 0:
      result = 1

    return result
