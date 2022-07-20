
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# already uses adjusted prices
mcdon = get_pricing('MCD', start_date='2005-01-01', end_date='2017-02-01', frequency='daily') # minute
mcdon['close_price'].plot()

mcdon['close_price'].pct_change(1).hist(bins=100)
mcdon_eq_info = symbols('MCD')
type(mcdon_eq_info)
mcdon_eq_info.to_dict()


# Quantopian IDE

# initialize maintains state of algo

def initialize(context):
  context.techies = [ sid(24), sid(1900), sid(16841) ]

  # context.aapl = sid(24)
  # context.csco = sid(1900)
  # context.amzn = sid(16841)

# called once after each minute
def handle_data(context, data):

  # grabs current data for use in algo
  tech_close = data.current(context.techies, 'close')
  print(tech_close)
  print('\n')
  print(type(tech_close))

  # is the current data = to date in my backtest
  print(data.is_stale(sid(24))

  # order_target_percent(context.aapl, .27)
  # order_target_percent(context.csco, .20)
  # order_target_percent(context.amzn, .53)

  # avoids common trading errors in backtest
  if data.can_trade(sid(16841)):
    order_target_percent(sid(16841, 1.0)



# PART 2
# called once after each minute
def handle_data(context, data):
  price_history = data.history(context.techies, fields='price', bar_count=5,frequency='1d')
  print(price_history)


def initialize(context):
  context.aapl = sid(24)

  schedule_funciton(open_positions, date_rules.every_week(), time_rules.market_open())
  schedule_funciton(close_positions, date_rules.weekend_end(), time_rules.market_close(minutes=30))

# set 10% AAPL
def open_positions(context, data):
  order_target_percent(context.aapl, 0.10)

# set 0% AAPL
def close_positions(context, data):
  order_target_percent(context.aapl, 0.0)


def initialize(context):
  context.amzn = sid(16841)
  context.ibm = sid(3766)

  schedule_function(rebalance, date_rules.every_day(), time_rules.market_open())
  schedule_function(record_vars, date_rules.every_day(), time_rules.market_close())

def rebalance(context, data):
  order_target_percent(context.amzn, 0.5)
  order_target_percent(context.ibm, -0.5)

def record_vars(context, data):
  record(amzn_close=data.current(context.amzn, 'close'))
  record(ibm_close_jelly=data.current(context.ibm, 'close'))

# other ops
# slippage -> liquidity penalty
# commisions







