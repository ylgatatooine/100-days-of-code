import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf

# Override pandas datareader with Yahoo Finance
yf.pdr_override()

# Fetch AAPL stock data from Yahoo Finance
aapl = pdr.get_data_yahoo("AAPL", start="2022-01-01", end="2023-01-01")

# Display the first few rows of the data
print(aapl.head())

# Accessing index and columns
aapl_index = aapl.index
aapl_columns = aapl.columns

# Selecting a subset of the 'Close' column
ts = aapl['Close'][-10:]
type_of_ts = type(ts)

# Calculate the difference between Open and Close and remove the column
aapl['diff'] = aapl.Open - aapl.Close
del aapl['diff']

# Plotting the 'Close' column
# import matplotlib.pyplot as plt
# aapl['Close'].plot(grid=True)
# plt.show()

# Calculate daily percentage change and log returns
daily_close = aapl[['Adj Close']]
daily_pct_c = daily_close.pct_change().fillna(0)
print(daily_pct_c)

daily_log_returns = np.log(daily_close.pct_change() + 1)
print(daily_log_returns)

# Resample data for monthly and quarterly analysis
monthly = aapl.resample("BM").apply(lambda x: x[-1])
print(monthly.pct_change())

quarterly = aapl.resample("4M").mean()
