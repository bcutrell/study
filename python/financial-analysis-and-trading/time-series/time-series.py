# Notes

# Trends
# Seasonality - repeating trends
# Cyclical - trends with no set repetition

# Stats Models
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm

df = sm.datasets.macrodata.load_pandas().data

# tsa - time series analysis
index = pd.Index(sm.tsa.datetools.dates_from_range('1959Q1', '2009Q3'))
df.index = index

df['realgdp'].plot()

gdp_cylce, gdp_trend = sm.tsa.filters.hpfilter(df['realgdp'])

df['trend']  = gdp_trend
df[['realgdp', 'trend']]['2000-03-31':].plot()

# ETS Models
# Error - Trend - Seasonality
#   Models will use these terms for smoothing and may add them, multiply them or just leave them out
# - Exponential Smoothing
# - Trend Methods Models
# - ETS Decomposition

# Breakdown
# -> Observed, Trend, Seasonal, Residual (error term)

airline = pd.read_csv('airline_passengers.csv', index_col="Month")
airline.dropna(inplace=True)
airline.index = pd.to_datetime(airline.index)

from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(airline['Thousands of Passengers'], model='multiplicative') # or additive
result.seasonal.plot()
result.trend.plot()
fig = result.plot()

# EWMA models
# - Expoenentially Weighted Moving Averages
#   - reduces the lag effect from SMA puts more weight on recent values
#   - adjusting the weight value is the key to using EWMA models

airline = pd.read_csv('airline_passengers.csv', index_col="Month")
airline.dropna(inplace=True)
airline.index = pd.to_datetime(airline.index)

airline['6-month-SMA'] = airline['Thousands of Passengers'].rolling(window=6).mean()
airline['12-month-SMA'] = airline['Thousands of Passengers'].rolling(window=12).mean()
airline.plot()

# span corresponds to what is commmonly called an N-day EW moving average
# alpha specified the smoothing factor directly
# half life is the period of time for the exponential weight to reduce to one half
# center of mass has a more physical interpretation and can be thought of in terms of span: c=(s-1)/2
airline['EWMA-12'] = airline['Thousands of Passengers'].ewm(span=12).mean()
airline[['Thousands of Passengers', 'EWMA-12']].plot()

# ARIMA Models
# auto regressive integrated moving average
# general do not work well with financial data
# non-seasonal and seasonal
# AR - regression task
# I differencing of observations
# MA observation and residual error

# Stationary data - constant mean and variance over time, covariance should not be a function of time
# You can keep diff X1 = n1 - n0 the data until it is stationary

# ARIMA inputs
# p: the number of lab observations
# d: number of times that the raw observations are differenced
# q: size of the MA window

# PACF - partial auto correlation function
# ACF - auto correlation function

# Autocorrelation plots
# 1. gradual decline
# 2. sharp drop-off

# ARIMA Code Along

df = pd.read_csv('monthly-milk-production-pounds-p.csv')
df.columns = ['Month', 'Milk in Pounds per Cow']
df.drop(168, axis=0, inplace=True)
df['Month'] = pd.to_datetime(df['Month'])
df.set_index('Month', inplace=True)
df.plot()

time_series = df['Milk in Pounds per Cow']
time_series.rolling(12).mean().plot(label='12 Month Rolling Mean')
time_series.rolling(12).std().plot(label='12 Month Rolling Mean')
time_series.plot()
plt.legend()

from statsmodels.tsa.seasonal import seasonal_decompose
decomp = seasonal_decompose(time_series)
fig = decomp.plot()

# Dickey Fuller Test
# null hypothesis: non stationary data
# large p value - fail to reject null
from statsmodels.tsa.stattools import adfuller
result = adfuller(df['Milk in Pounds per Cow'])

def adf_check(time_series):
  result = adfuller(time_series)
  print('Augmented Dicky-Fuller Test')
  labels = ['ADF Test Statistic', 'p-value', '# of lags', 'Num of Observations user']

  for value, label in zip(result,labels):
    print(label+ " : "+str(value))

  if result [1] <= 0.05:
    print("Strong evidence agaisnt null hypothesis")
    print("reject null hypothesis")
    print("Data has no unit root and is stationary")
  else:
    print("Weak evidence agaisnt null hypothesis")
    print("Fail to reject null hypothesis")
    print("Data has a unit root and is non-stationary")


adf_check(df['Milk in Pounds per Cow'])

df['First Difference'] = df['Milk in Pounds per Cow'] - df['Milk in Pounds per Cow'].shift(1)

df['First Difference'].plot()
adf_check(df['First Difference'].dropna())

df['Second Difference'] = df['First Difference'] - df['First Difference'].shift(1)
adf_check(df['Second Difference'].dropna())

df['Seasonal Difference'] = df['Milk in Pounds per Cow'] - df['Milk in Pounds per Cow'].shift(12)
adf_check(df['Seasonal Difference'].dropna())

df['Seasonal First Difference'] = df['First Difference'] - df['First Difference'].shift(12)
adf_check(df['Seasonal First Difference'].dropna())

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
fig_first = plot_acf(df['First Difference'].dropna())

from pandas.plotting import autocorrelation_plot
autocorrelation_plot(df['Seasonal First Difference'])

result = plot_pacf(df['Seasonal First Difference'].dropna())

# ARIMA code
plot_acf(df['Seasonal First Difference'].dropna())
plot_pacf(df['Seasonal First Difference'].dropna())

from statsmodels.tsa.arima_model import ARIMA

# Seasonal ARIMA
sm.tsa.statespace.SARIMAX(df['Milk in Pounders per Cow'], order=(0,1,0),seaonsal_order=(1,1,1,12))
results = model.fit()
print(results.summary())

results.resid # residual values
results.resid.plot(kind='kde')
df['forecast'] = reuslts.predict(start=150, end=168)

# Display forecast
df[['Milk in Pounders per Cow', 'forecast']].plot() 

df.tail()
# add months with empty values to use forecast
from pandas.tseries.offsets import DateOffset

# create list of timestamps
future_dates = [ df.index[-1] + DateOffset(months=x) for x in range(1,24) ]

future_df = pd.Dateframe(index=future_dates, columns=df.columns)
final_df = pd.concat([df, future_df])

final_df['forecast'] = results.predict(start=168, end=192)

final_df[['Milk in Pounders per Cow', 'forecast']].plot()

# Why aren't arima values good for financial data?
# - doesnt account for outside forces such as random increases in volume trades

