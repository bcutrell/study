import pandas as pd
import numpy as np
from pandas_datareader.data import DataReader
import datetime as dt

#
# Goal: Generate etf data files that can be used for testing portfolio optimizations
#
# Input: The product screener file from https://www.ishares.com/us/resources/tools
#   * For some reason, the xls file produced from the site is in the 2004 excel XML format
#   the easiest way to fix this is to open the file in excel and save as a csv
# Output: prices.csv
#         etf_info.csv
#

def get_price_df(ticker):
    return DataReader(ticker, 'iex',
                      dt.datetime(2014, 1, 1),
                      dt.datetime.now(),
                      retry_count=0) # .reset_index()


OUTPUT_COLUMNS = [
        'Asset Class', 
        'CUSIP', 
        'Ticker', 
        'Fees', 
        'Asset Class', 
        'Sub Asset Class', 
        'Inception Date', 
        'Market', 
        'Country', 
        'Fees'
]

if __name__ == '__main__':

    # read in screener
    df = pd.read_csv('ProductScreener.csv')
    df = df[OUTPUT_COLUMNS] # drop unused cols

    # drop the row containing the subheaders that we don't care about
    df.drop(index=0, inplace=True)

    # get a list of tickers ordered by inception date
    df['Inception Date'] = pd.to_datetime(df['Inception Date'])
    df.sort_values(by=['Inception Date'], inplace=True)
    tickers = df['Ticker'].values.flatten()

    # initialize our prices df for the ticker with the longest history
    ticker = tickers[0]
    tickers = np.delete(tickers,0) # pop(0) doesn't work with np arrays
    price_df = get_price_df(ticker)
    prices_df = pd.DataFrame(index=price_df.index)
    prices_df[ticker] = price_df['close']

    # add in the other tickers
    for ticker in tickers:
        price_df = get_price_df(ticker)
        prices_df[ticker] = price_df['close']

    # output prices.csv and etf_info.csv
    prices_df.to_csv('prices.csv')
    df.to_csv('etf_info.csv')

