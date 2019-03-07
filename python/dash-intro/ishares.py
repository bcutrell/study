import pandas as pd
import numpy as np
import requests
import config

import datetime as dt
from io import StringIO
import urllib
import code
import json

import time

#
# Goal: Generate etf data files that can be used for testing portfolio optimizations
#
# Input: The product screener file from https://www.ishares.com/us/resources/tools
#   * For some reason, the xls file produced from the site is in the 2004 excel XML format
#   the easiest way to fix this is to open the file in excel and save as a csv
# Output: prices.csv
#         etf_info.csv
#

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

BASE_URL = 'https://www.alphavantage.co/query?'

def url_for(ticker):
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'datatype': 'csv',
        'outputsize': 'full', # compact
        'apikey': config.ALPHAVANTAGE_API_KEY,
        'symbol': ticker 
    }
    return BASE_URL + urllib.parse.urlencode(params)

# standard API call frequency is 5 calls per minute and 500 calls per day
def get_price_df(ticker):
    attempts = 0

    while attempts < 3:
        resp = requests.get(url_for(ticker))
        # if we get a json response instead of application/x-download
        # we have reached the limit
        if resp.headers['Content-Type'] == 'application/json':
            attempts += 1
            print('Waiting due to API call frequency... ', ticker)
            time.sleep(30)
        else:
            df = pd.read_csv(StringIO(resp.text))
            df.index = pd.to_datetime(df.timestamp)
            return df

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
    tickers = np.delete(tickers, 0) # pop(0) doesn't work with np arrays

    price_df = get_price_df(ticker)
    prices_df = pd.DataFrame(index=price_df.index)
    prices_df[ticker] = price_df['adjusted_close']

    # add in the other tickers
    for ticker in tickers:
        price_df = get_price_df(ticker)
        prices_df[ticker] = price_df['adjusted_close']

    # output prices.csv and etf_info.csv
    prices_df.to_csv('prices.csv')
    df.to_csv('etf_info.csv')

