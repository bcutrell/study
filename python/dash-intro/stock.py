import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime as dt
import plotly.graph_objs as go

from pandas_datareader.data import DataReader
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

import requests
import json


def get_stock_df(ticker):
  df = DataReader(str(ticker), 'iex',
                  dt.datetime(2018, 1, 1),
                  dt.datetime.now(),
                  retry_count=0).reset_index()

  return df

def ticker_options():
    resp = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
    return [ {'label': i["symbol"], 'value': i["symbol"] }  for i in json.loads(resp.text) ]

external_stylesheets = ['https://unpkg.com/nes.css@2.0.0/css/nes.min.css']

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
    app.run_server(debug=True)