# Exchange Simulator
Simulator of a currency exchange. It supports fees and minimum order amounts.

One currency acts as a base and is called as a _cash_. In our example it's BTC. Prices of other currencies expressed in a cash currency. You can trade only within cash currency pairs. Trading occurs at close prices.


## Usage

Install dependencies:

```bash
pip3 install -r requirements.txt
```
Sample data is located in `sample_data` directory and it was downloaded via `download_sample` script. Each currency candles must be saved in a separate csv file, but it can contain different number of fields and columns (for example, it can contain only open and close prices).

Now we can trade.

```python
from exchange import Exchange

cash_amount = 1  # How much of base currency (cash) we will have.
fee = 0.09       # Fee in percents for each trade (0.09%).
data_path = 'sample_data'  # Where csv files with data are stored.

# Minimum trade volume expressed in a base currency (cash).
min_order_size = 0.0001

# List of currecies to use.
currencies = ['ETC', 'ETH', 'LTC', 'XMR']

# Create an exchange. We are at the first candle now.
ex = Exchange(cash_amount, fee, min_order_size, data_path, currencies)

# You can print current candle for a particular currency.
print(ex.current_candles['ETC'])

# Print a current balance.
print(ex.balance)

# buy/sell operation will return 0 if it was executed successfully,
# 1 - not enough funds,
# 2 - order is smaller than the minimum,
# 3 - not enough funds and order is smaller than the minimum.
print(ex.buy('ETC', 100))
print(ex.buy('LTC', 50))

# Check balance again.
print(ex.balance)

# All done, now we want to wait for 30 time periods. This operation will
# also return 0 in case of success and 1 if we are at the end of data.
for _ in range(30):
  ex.next_step()

# Now we want to sell.
print(ex.sell('ETC', 100))
print(ex.sell('LTC', 50))

# We made some money, yeah!
print(ex.balance)
```
