import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dash.dependencies import Input, Output, State

import pandas as pd
from pandas_datareader.data import DataReader
import numpy as np

import requests_cache
import requests

import datetime as dt
import json
import code

class Portfolio(object):

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
        # TODO 
        # store parts of the df so that calculations do not need to be repeated

        for ticker in self.tickers:
            df = self.get_prices_df(ticker)
            df['return'] = df['close'].pct_change(1)
            df['cumulative'] = df['close']/df['close'].iloc[0]

            data.append(
                go.Scatter(x=df['date'], y=df['cumulative'], name=ticker)
            )

        return data


def ticker_options():
    resp = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
    return [ {'label': i["symbol"], 'value': i["symbol"] }  for i in json.loads(resp.text) ]


# Use the awesome nes css library
external_stylesheets = [
        'https://fonts.googleapis.com/css?family=Press+Start+2P', 
        'https://unpkg.com/nes.css@2.0.0/css/nes.min.css'
]

#
# Setup Dash App and Layout
#
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = \
html.Div(children=[
    html.Div([
        html.P('Stock Market Dashboard', className='title'),
        html.Div([
            html.Label('Pick some stocks:'),
            dcc.Dropdown(
                id='my-dropdown',
                options= ticker_options(),
                multi=True,
                value=['AAPL']
            )], className='nes-field'),

        html.Div([
            html.Label('Select a start and end date:'),
            dcc.DatePickerRange(id='my-date-picker',
                                min_date_allowed=dt.datetime(2015,1,1),
                                max_date_allowed=dt.datetime.today(),
                                start_date=dt.datetime(2018,1,1),
                                end_date=dt.datetime.today()),
            html.Button(id='submit-button', n_clicks=0, className='nes-btn', children='Submit'),
        ], className='nes-field'),

        html.Div(id='output-container'),
        dcc.Graph(id='my-graph')],
    className='nes-container with-title')
])

# Use object to store DataReader calls
# and perform any dataframe calculations
portfolio = Portfolio('AAPL')

#
# Callbacks
#
@app.callback(Output('my-graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('my-dropdown', 'value'),
               State('my-date-picker', 'start_date'),
               State('my-date-picker', 'end_date')])
def update_closing_prices(n_clicks, tickers, start_date, end_date):

    # not used for now...
    start_date = dt.datetime.strptime(start_date[:10], '%Y-%m-%d')
    end_date = dt.datetime.strptime(end_date[:10], '%Y-%m-%d')

    portfolio.set_tickers(tickers)

    return {
        'data': portfolio.traces(),
        'layout': go.Layout()
    }

def update_daily_returns(tickers):
    pass

def update_factory_analysis():
    pass

def update_optimal_allocation():
    pass

def update_trailing_graphs():
    pass

def update_simple_analysis():
    pass # sharpe, capm, et.c

if __name__ == '__main__':
    app.run_server(debug=True)

