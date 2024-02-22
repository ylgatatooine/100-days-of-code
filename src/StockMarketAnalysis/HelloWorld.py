import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

from pandas_datareader import data as pdr

import yfinance as yf
yf.pdr_override()

aapl = pdr.get_data_yahoo("AAPL", start = "2022-01-01", end="2023-01-01")

print(aapl.head())

aapl.index
aapl.columns
ts = aapl['Close'][-10:]
type(ts)

aapl['diff'] = aapl.Open - aapl.Close
del aapl['diff']

# import matplotlib.pyplot as plt
# aapl['Close'].plot(grid = True)
# plt.show()

daily_close = aapl[['Adj Close']]
daily_pct_c = daily_close.pct_change()
daily_pct_c.fillna(0, inplace=True)
print(daily_pct_c)
daily_log_returns = np.log(daily_close.pct_change()+1)
print(daily_log_returns)


monthly = aapl.resample("BM").apply(lambda x: x[-1])
monthly.pct_change()
print(monthly)

quarter = aapl.resample("4M").mean()
quarter.pct_change()
print(quarter)

import matplotlib.pyplot as plt
daily_pct_c.hist(bins=50)
plt.show()
print(daily_pct_c.describe())