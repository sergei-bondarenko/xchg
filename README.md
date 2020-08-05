# Exchange Simulator
[![Build Status](https://github.com/sergei-bondarenko/xchg/workflows/build/badge.svg?branch=master&event=push)](https://github.com/sergei-bondarenko/xchg/actions?query=workflow%3Abuild)

Simulator of a currency exchange. It supports fees and minimum order amounts.

One currency acts as a base and is called as a _cash_. In our example it's BTC. Prices of other currencies expressed in a cash currency. You can trade only within cash currency pairs. Trading occurs at close prices.
