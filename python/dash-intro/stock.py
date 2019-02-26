import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime as dt
import plotly.graph_objs as go
from pandas_datareader.data import DataReader
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import requests_cache
import requests
import json

import datetime
import code

external_stylesheets = ['https://unpkg.com/nes.css@2.0.0/css/nes.min.css']

expire_after = datetime.timedelta(days=3)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
master_df = pd.DataFrame()

def get_stock_df(ticker):
    stock_df = DataReader(str(ticker), 'iex',
                    dt.datetime(2018, 1, 1),
                    dt.datetime.now(),
                    session=session,
                    retry_count=0).reset_index()
    # add values to master_df
    master_df['date'] = stock_df.date
    master_df[ticker] = stock_df['close'] # adj close?

    return stock_df

def ticker_options():
    resp = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
    return [ {'label': i["symbol"], 'value': i["symbol"] }  for i in json.loads(resp.text) ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    dcc.Dropdown(
        id='my-dropdown',
        options= ticker_options(),
        multi=True
    ),
    html.Div(id='output-container')
])

# @app.callback(  Output(),
#                 [Input()])
def ticker_select_callback(ticker):
    pass

if __name__ == '__main__':
    # app.run_server(debug=True)
    get_stock_df('AAPL')
    code.interact(local=locals())