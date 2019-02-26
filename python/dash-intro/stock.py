'''
Completion <C-Space>
Goto assignments <leader>g (typical goto function)
Goto definitions <leader>d (follow identifier as far as possible, includes imports and statements)
Show Documentation/Pydoc K (shows a popup with assignments)
Renaming <leader>r
Usages <leader>n (shows all the usages of a name)
Open module, e.g. :Pyimport os (opens the os module)
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dash.dependencies import Input, Output

import pandas as pd
from pandas_datareader.data import DataReader
import numpy as np

import requests_cache
import requests

import datetime as dt
import json
import code

class PricesDataFrame(object):

    def __init__(self, initial_ticker):
        expire_after = dt.timedelta(days=3)
        self.session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)

        self.df = self.get_prices_df(initial_ticker)

    def set_tickers(self, tickers):
        self.tickers = tickers

    def get_prices_df(self, ticker):
        return DataReader(str(ticker), 'iex',
                          dt.datetime(2018, 1, 1),
                          dt.datetime.now(),
                          session=self.session,
                          retry_count=0).reset_index()

    def traces(self):
        data = [] # list of traces
        for ticker in self.tickers:
            df = self.get_prices_df(ticker)
            data.append(
                go.Scatter(x=df['date'], y=df['close'], name=ticker)
            )

        return data


def ticker_options():
    resp = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
    return [ {'label': i["symbol"], 'value': i["symbol"] }  for i in json.loads(resp.text) ]


# Use the awesome nes css library
external_stylesheets = ['https://unpkg.com/nes.css@2.0.0/css/nes.min.css']

#
# Setup Dash App and Layout
#
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = \
html.Div(children=[
    dcc.Dropdown(
        id='my-dropdown',
        options= ticker_options(),
        multi=True,
        value=['AAPL']
    ),
    html.H1('Closing Prices'),
    html.Div(id='output-container'),
    dcc.Graph(id='my-graph')
])

# Use object to store DataReader calls
# and perform any dataframe calculations
prices_df = PricesDataFrame('AAPL')

#
# Callbacks
#
@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(tickers):
    prices_df.set_tickers(tickers)

    return {
        'data': prices_df.traces(),
        'layout': go.Layout()
    }


if __name__ == '__main__':
    # TODO CAPM + factor regressions, trailing n graphs, sharpe ratio, optimal allocations
    app.run_server(debug=True)

