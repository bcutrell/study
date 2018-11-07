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

# On Index
pd.merge(df_left, df_right, left_on='key', right_index=True)
# left on can accept list for nested indicies

# Join
df_left.join(df_right)

##############################
# Concatenate
##############################
arr1 = np.arange(9).reshape(3,3)
np.concatenate([arr1,arr1],axis=1) # left to right
np.concatenate([arr1,arr1],axis=0) # top to bottom

pd.concat([ser1, ser2], axis=1)
pd.concat([ser1, ser2], keys=['cat1', 'cat2'])

pd.concat([dframe1, dframe2], keys=['cat1', 'cat2'], ignore_index=True)

##############################
# Combine DataFrames
##############################
ser1.combine_first(ser2)
dframe_odds.combine_first(dframe_evens)

##############################
# Reshaping
##############################
df.stack()
df.unstack() # can pass in column name

##############################
# Pivot
##############################

# args: rows, columns, field value
dfame.pivot('date', 'variable', 'value')

##############################
# Duplicates
##############################
dframe.duplicated() # returns boolean df
dframe.drop_duplicates() # removes false values from duplicated()
dframe.drop_duplicates(['key1']) # drop from key1 column
dframe.drop_duplicates(['key1'], take_last=True) # keep last dup

##############################
# Mapping
##############################

dframe['state'] = dframe['city'].map(state_map)
# create a new column based on keys / values in state_map dict

##############################
# Replace
##############################

ser1.replace(1, np.nan)
ser1.replace([1,4], [100, 400])
ser1.replace({ 4: np.nan })

##############################
# Rename Index
##############################

dframe.index.map(str.lower)
dframe.index = dframe.index.map(str.lower) # mutuate
dframe.rename(index=str.title, columns=str.lower)
dframe.rename(index={'ny': 'NEW YORK'}, columns={ 'A': 'ALPHA'})

##############################
# Binning
##############################

decade_cat = pd.cut(years, decade_bins)
decade_cat.categories
pd.value_counts(decade_cat)
pd.cut(years,2,percision=1)

