import pandas as pd
from pandas import Series, DataFame

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
# %matplotlib inline

from pandas.io.data import DataReader
from datetime import datetime

tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

end = dateimte.now()
start = dateimte(end.year-1, end.month, end.day)

for stock in tech_list:
  globals()[stock] = DataReader(stock, 'yahoo', start, end)

GOOG.header()


# http://nbviewer.jupyter.org/github/jmportilla/Udemy-notes/blob/master/Data%20Project%20-%20Stock%20Market%20Analysis.ipynb
# http://www.quantatrisk.com/financial-risk-management/
def collect_stock_data():
  pass

AAPL['Adj Close'].plot(legend=True, figsize=(18,4))
AAPL['Volume'].plot(legend=True, figsize=(18,4))

if __name__ == '__main__':
  print('hello')
