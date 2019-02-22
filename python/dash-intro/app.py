# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime as dt
import plotly.graph_objs as go

from pandas_datareader.data import DataReader
from dash.dependencies import Input, Output
import pandas as pd

# https://dash.plot.ly/getting-started
# https://github.com/plotly/dash-stock-tickers-demo-app/blob/master/app.py

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.RangeSlider(
        id='range-slider',
        min=-5,
        max=6,
        marks={i: str(i) for i in range(-5,7)},
        value=[-3,4]
    ),
    html.H1(id='product'),
    html.P(),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': 'pink',
                'paper_bgcolor': 'yellow',
                'font': 'blue',
                'title': 'Dash Data Visualization'
            }
        }
    )
])


def get_stock_df(ticker='AAPL'):
  df = DataReader(str(ticker), 'yahoo',
                  dt.datetime(2017, 1, 1),
                  dt.datetime.now(),
                  retry_count=0).reset_index()

  return df

@app.callback(  Output('product', 'children'),
                [Input('range-slider', 'value')]
            )
def update_value(value_list):
    return value_list[0]*value_list[1]


if __name__ == '__main__':
    df = get_stock_df()
    print(df.head())
    app.run_server(debug=True)

