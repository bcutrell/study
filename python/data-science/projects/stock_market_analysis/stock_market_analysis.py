import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
# %matplotlib inline

# from pandas.io.data import DataReader
from pandas_datareader.data import DataReader
from datetime import datetime

# Fama/French Data
# DataReader('5_Industry_Portfolios', 'famafrench')

def collect_stock_data():
    tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
    end = datetime.now()
    start = datetime(end.year-1, end.month, end.day)
    for stock in tech_list:
      globals()[stock] = DataReader(stock, 'quandl', start, end)

def adj_close_plot(stock_df):
    stock_df['Adj Close'].plot(legend=True, figsize=(18,4))

def volume_plot(stock_df):
    stock_df['Adj Close'].plot(legend=True, figsize=(18,4))

def ma_plot(stock_df):
    stock_df[['Adj Close','MA for 10 days','MA for 20 days','MA for 50 days']].plot(subplots=False,figsize=(10,4))

def daily_return_plot(stock_df):
    stock_df['Daily Return'].plot(figsize=(12,4),legend=True,linestyle='--',marker='o')

def daily_distplot(stock_df):
    sns.distplot(stock_df['Daily Return'].dropna(), bins=100, color='purple')

def set_ma(stock_df, ma_day=[10,20,50]):
    for ma in ma_day:
        column_name = "MA for %s days" %(str(ma))
        stock_df[column_name]=pd.rolling_mean(stock_df['Adj Close'],ma)

def set_daily_return(stock_df):
    stock_df['Daily Return'] = AAPL['Adj Close'].pct_change()

if __name__ == '__main__':
    collect_stock_data()
    print(AAPL)

