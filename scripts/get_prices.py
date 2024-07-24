import yfinance as yf
import pandas as pd

# Define the ticker symbol
ticker_symbol = 'IVV'

# Get the current date
current_date = pd.Timestamp.today().strftime('%Y-%m-%d')

# Define the start date (beginning of the year)
start_date = pd.Timestamp.today().replace(month=1, day=1).strftime('%Y-%m-%d')

# Download the YTD daily prices
ivv_data = yf.download(ticker_symbol, start=start_date, end=current_date)

# Save the data to a CSV file
ivv_data.to_csv('ivv.csv')
