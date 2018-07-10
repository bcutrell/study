# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime as dt

from pandas_datareader.data import DataReader
import pandas as pd

# https://dash.plot.ly/getting-started
# https://github.com/plotly/dash-stock-tickers-demo-app/blob/master/app.py

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])


def get_stock_df(ticker='AAPL'):
  df = DataReader(str(ticker), 'morningstar',
                  dt.datetime(2017, 1, 1),
                  dt.datetime.now(),
                  retry_count=0).reset_index()

  return df

if __name__ == '__main__':
    app.run_server(debug=True)

