import numpy as pd
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

my_year = 2017
my_month = 1
my_day = 2
my_hour = 13
my_minute = 30
my_second = 15

my_date = datetime(my_year, my_month, my_day)
my_date.day

first_two = [ datetime(2016,1,1), datetime(2016,1,2)]

# Datetime Index
dt_ind = pd.DatetimeIndex(first_two)

data = np.random.randn(2,2)
cols = ['a', 'b']

df = pd.DataFrame(data, dt_ind, cols)
df.index.argmax() # latest index (use min for first)
df.index.max() # latest date


# Time Resampling
df = pd.read_csv('data/walmart_stock.csv') # parse_dates=True, index_col='Date'
df.info()

df['Date'] = pd.to_datetime(df['Date'], format='')
df['Date'] = df['Date'].apply(pd.to_datetime)

df.set_index('Date', inplace=True)
df.head()

df.resample(rule='A').mean() # year end frequency
# Q - quaterly 
# BQ - business quaterly

def first_day(entry):
  return entry[0]

df.resample('A').apply(first_day)

df['Close'].resample('A').mean().plot(kind='bar')

# Time Shifts
df.shift(periods=1) # one index row
df.head()

df.tshift(freq='M') # shifts index

# Rolling and Expanding

df.rolling(7).mean().head(20) # moving average for each week
df.rolling(window=7).mean()['Close'] # moving average for each week

df['Close 30 Day MA'] = df['Close'].rolling(window=7).mean()
df[['Close 30 Day MA', 'Close']].plot(figsize(16,16))

df['Close'].expanding().mean().plot(figsize=(16,6))

# Bollinger Bands

# Close 20 MA
df['Close: 20 Day Mean'] = df['Close'].rolling(20).mean()

# Upper = 20MA + 2*std(20)
df['Upper'] = df['Close: 20 Day Mean'] + 2*(df['Close'].rolling(20).std())

# Lower = 20MA - 2*std(20)
df['Lower'] = df['Close: 20 Day Mean'] - 2*(df['Close'].rolling(20).std())

df[['Close', 'Close: 20 Day Mean', 'Upper', 'Lower']].plot(figsize=(16,6))

