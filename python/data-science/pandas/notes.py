import numpy as np
import pandas as pd
from pandas import Series,DataFrame

# Reading and Writting Files
dframe = pd.read_csv('demo.csv', header=None)
dframe = pd.read_table('demo.csv', sep=',', header=None)

# dframe.to_csv('mytextdata_out.csv')
import sys
dframe.to_csv(sys.stdout, sep='_')
dframe.to_csv(sys.stdout, sep='?')
dframe.to_csv(sys.stdout, columns=[0,1,2])

json_obj = """
{"menu": {
  "id": "file",
  "value": "File",
  "popup": {
    "menuitem": [
    {"value": "New", "onclick": "CreateNewDoc()"},
    {"value": "Open", "onclick": "OpenDoc()"},
    {"value": "Close", "onclick": "CloseDoc()"}
    ]
  }
}}
"""

import json

data = json.loads(json_obj)
json.dumps(data)

from pandas import read_html

# pip install beautiful-soup
# pip install html5lib
url = "https://www.fdic.gov/bank/individual/failed/banklist.html"

dframe_list = pd.io.html.read_html(url)
dframe = dframe_list[0]
dframe.columns.values

# pip install xLrd
# pip install openpyxL
xlsfile = pd.ExcelFile('test.xlsx')
dframe = xlsfile.parse('Sheet1')
