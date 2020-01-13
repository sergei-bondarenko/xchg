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
