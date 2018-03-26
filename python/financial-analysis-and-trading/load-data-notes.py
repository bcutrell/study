
# PANDAS
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2015,1,1) 
end = datetime.datetime(2017,1,1)

facebook = web.DataReader('FB', 'google', start, end)
facebook.head()

from pandas_datareader.data import Options
fb_options = Options('FB', 'google')
options_df = fb_options.get_options_data(expiry=fb_options.expiry_dates[0])
options_df.head()

# QUADL
import quandl
mydata = quandl.get('EIA/PET_RWTC_D')
# can use , returns='numpy'
import matplotlib.pyplot as plt
mydata.plot()

mydata = quandl.get('ZILLOW/C9_ZRIFAH')

mydata = quandl.get('WIKI/AAPL')
my.head()

