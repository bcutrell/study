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

def tech_summary():
    closing_df = DataReader(['AAPL','GOOG','MSFT','AMZN'],'yahoo',start,end)['Adj Close']
    tech_rets = closing_df.pct_change()

    # from IPython.display import SVG
    # SVG(url='http://upload.wikimedia.org/wikipedia/commons/d/d4/Correlation_examples2.svg')
    sns.jointplot('GOOG','GOOG',tech_rets,kind='scatter',color='seagreen')
    sns.jointplot('GOOG','MSFT',tech_rets,kind='scatter')
    sns.pairplot(tech_rets.dropna())

    # Set up our figure by naming it returns_fig, call PairPLot on the DataFrame
    returns_fig = sns.PairGrid(tech_rets.dropna())

    # Using map_upper we can specify what the upper triangle will look like.
    returns_fig.map_upper(plt.scatter,color='purple')

    # We can also define the lower triangle in the figure, inclufing the plot type (kde) or the color map (BluePurple)
    returns_fig.map_lower(sns.kdeplot,cmap='cool_d')

    # Finally we'll define the diagonal as a series of histogram plots of the daily return
    returns_fig.map_diag(plt.hist,bins=30)

    # Set up our figure by naming it returns_fig, call PairPLot on the DataFrame
    returns_fig = sns.PairGrid(closing_df)

    # Using map_upper we can specify what the upper triangle will look like.
    returns_fig.map_upper(plt.scatter,color='purple')

    # We can also define the lower triangle in the figure, inclufing the plot type (kde) or the color map (BluePurple)
    returns_fig.map_lower(sns.kdeplot,cmap='cool_d')

    # Finally we'll define the diagonal as a series of histogram plots of the closing price
    returns_fig.map_diag(plt.hist,bins=30)

    # Let's go ahead and use sebron for a quick correlation plot for the daily returns
    sns.corrplot(tech_rets.dropna(),annot=True)

    return tech_rets

def tech_risk(tech_rets):
    pass


if __name__ == '__main__':
    collect_stock_data()
    print(AAPL)

