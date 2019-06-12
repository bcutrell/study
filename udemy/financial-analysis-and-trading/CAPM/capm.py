# Capital Asset Pricing Model

# rt = B*rm + alpha

# rm = return market
# B = beta
# alpha = residual alphta term



# Code along

# CAPM can almost be treated as a simple linear regression

from scipy import stats
help(stats.linregress)

import pandas as pd
import pands_datareader as web

spy_etf = web.DataReader('SPY', 'google')

start = pd.to_datetime('2010-01-04')
end = pd.to_datetime('2017-07-25')

aapl = web.DataReader('AAPL', 'google')

import matplotlib.pyplot as plt

aapl['Close'].plot(label='AAPL')
spy_etf['Close'].plot(label='SPY Index')
plt.legend()

aapl['Cumulative'] = aapl['Close']/aapl['Close'].iloc[0]
spy_etf['Cumulative'] = spy_etf['Close']/spy_etf['Close'].iloc[0]

aapl['Cumulative'].plot(label='AAPL')
spy_etf['Cumulative'].plot(label='SPY Index')
plt.legend()

aapl['Daily Return'] = aapl['Close'].pct_change(1)
spy_etf['Daily Return'] = spy_etf['Close'].pct_change(1)

plot.scatter(aapl['Daily Return'], spy_etf['Daily Return'], alpha=0.25)

beta, alpha, r_vaule, p_value, std_err = stats.linregress(aapl['Daily Return'].iloc[1:], spy_etf['Daily Return'].iloc[1:])
# Higher beta -> more like the market

import numpy as np

noise = np.random.normal(0,0.001, len(spy_etf['Daily Return'].iloc[1:]))

fake_stock = spy_etf['Daily Return'].iloc[1:] + noise
plot.scatter(fake_stock, spy_etf['Daily Return'], alpha=0.25)

beta, alpha, r_vaule, p_value, std_err = stats.linregress(fake_stock, spy_etf['Daily Return'].iloc[1:])

# beta ~ 1
