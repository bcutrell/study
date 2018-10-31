import numpy as np
import pandas as pd
from pandas import Series,DataFrame

##############################
# Reading and Writting Files
##############################
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

##############################
# Merge
##############################
dframe1 = Dataframe({'key': ['X', 'Z', 'Y', 'Z', 'X', 'X'], 'data_set_1': np.arange(6) })
dframe2 = DataFrame({'key': ['Q', 'Y', 'Z'], 'data_set_2': [1,2,3] })

# overlaps where keys match
pd.merge(dframe1, dframe2)
pd.merge(dframe1, dframe2, on='key')
pd.merge(dframe1, dframe2, on='key', how='left') # 6 entries
pd.merge(dframe1, dframe2, on='key', how='right') # 3 entries
pd.merge(dframe1, dframe2, on='key', how='outer') # 7 entries (union)

dframe3 = Dataframe({'key': ['X', 'X', 'X', 'Y', 'Z', 'Z'], 'data_set_3': np.arange(6) })
dframe4 = Dataframe({'key': ['Y', 'Y', 'X', 'X', 'Z'], 'data_set_4': np.arange(5) })
pd.merge(dframe3, dframe4)

df_left = Dataframe({'key1': ['SF', 'SF', 'LA'],'key2': ['one', 'two', 'one'], 'left_data':[10,20,30]  })
df_right = Dataframe({'key1': ['SF', 'SF', 'LA', 'LA'],'key2': ['one', 'one', 'one', 'two'], 'right_data':[40,50,60, 70] })

pd.merge(df_left, df_right, on=['key1', 'key2'], how='outer')

pd.merge(df_left, df_right, on='key1')
pd.merge(df_left, df_right, on='key1', suffixes=('_lefty', '_righty'))


