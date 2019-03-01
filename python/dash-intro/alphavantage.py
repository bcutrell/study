import requests
import urllib
import config
import csv
import pandas as pd
from io import StringIO

import code

BASE_URL = 'https://www.alphavantage.co/query?'

def url_for(ticker):
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'datatype': 'csv',
        'outputsize': 'compact',
        'apikey': config.ALPHAVANTAGE_API_KEY,
        'symbol': ticker 
    }
    return BASE_URL + urllib.parse.urlencode(params)

resp = requests.get(url_for('AAPL'))
df = pd.read_csv(StringIO(resp.text))

