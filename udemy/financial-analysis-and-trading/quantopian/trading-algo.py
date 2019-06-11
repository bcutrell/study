# Pairs trading strategy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

start ='2015-01-01'
end= '2017-01-01'

united = get_pricing('UAL', start_date=start, end_date=end, frequency='daily')
american = get_pricing('AAL', start_date=start, end_date=end, frequency='daily')

american['close_price'].plot(label="AA")
united['close_price'].plot(label="United")
plt.legend()

# How correlated are these stocks?
# IRL - we would focus more on co integration

np.corrcoef(american['close_price'], united['close_price'])
spread = american['close_price'] - united['close_price']

spread.plot(label='Spread')
plt.axhline(spread.mean(), c='r')

# normalize averages
def zscore(stocks):
  return (stocks-stocks.mean()) / np.std(stocks))

zscore(spread).plot()
plt.axhline(zscore(spread).mean(), color='black')
plt.axhline(1.0, ls='--', c='g')
plt.axhline(-1.0, ls='--', c='r')

spread_mavg1 = spread.rolling(1).mean()
spread_mavg30 = spread.rolling(30).mean()

std_30 = spread.rolling(30).std()

# rolling z score
zcore_30_1 = (spread_mavg1-spread_mavg30)/30
zcore_30_1.plot(label='Rolling 30 Day Z score')
plt.axhline(0, ls='--', c='r')
plt.axhline(1.0, ls='--', c='black')

# implment stategy

# initialize - schedule_function
def initialize(context):
  schedule_function(check_pairs, date_rules.every_day(), time_rules.market_close(minutes=60))

  context.aa = sid(45971)
  context.ual = sid(28051)

  context.long_on_spread = False
  context.shorting_spread = False

#check_pair
def check_pairs(context,data):
  aa = context.aa
  ual = context.ual

  prices = data.history([aa,ual], 'price', 30, '1d')

  short_prices = prices.iloc[-1:]

  # spread
  mavg_30 = np.mean(prices[aa] - prices[ual])
  std_30 = np.std(prices[aa] - prices[ual])
  mavg_1 = np.mea(short_prices[aa] -short_prices[ual])

  # z score
  if std_30 > 0:
    zscore = (mavg_1 - mavg_30) / std_30

    if zscore > 0.5 and not context.shorting_spread:
      # spread = AA - UAL
      order_target_percent(aa, -0.5)
      order_target_percent(ual, 0.5)
      context.shorting_spread = True
      context.long_on_spread = False

    elif zscore < 1.0 and not context.long_on_spread:
      order_target_percent(aa, 0.5)
      order_target_percent(ual, -0.5)
      context.shorting_spread = False
      context.long_on_spread = True

    elif abs(zscore) < 0.1:
      order_target_percent(aa, 0)
      order_target_percent(ual, 0)
      context.shorting_spread = False
      context.long_on_spread = False

  record(Z_score = z_score)
