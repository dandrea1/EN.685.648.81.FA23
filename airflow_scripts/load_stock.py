# # Stock Data ETL

# #### This notebook uses the Yahoo Finance API to pull historical stock market data for the S&P 500 index. Then, I group by week and write out the data to a csv file which is then stored in a database. 

# %%
import pandas as pd
import numpy as np
import yfinance as yf
from pandas_datareader import data as pdr
from datetime import datetime, timedelta

# #### The line below downloads data for the S&P 500 (stock ticker SPY) dating from 2020-01-01 to 2023-11-24.
def previous_week_range():
    """Returns the start and end date of the previous week in YYYY-MM-DD format."""
    today = datetime.today()
    start_of_this_week = today - timedelta(days=today.weekday())  # Monday
    end_of_last_week = start_of_this_week - timedelta(days=1)  # Sunday
    start_of_last_week = end_of_last_week - timedelta(days=6)  # Previous Monday
    return start_of_last_week.strftime('%Y-%m-%d'), end_of_last_week.strftime('%Y-%m-%d')

if __name__ == "__main__":
    bdate, edate = previous_week_range()
    data = yf.download("SPY", start=bdate, end=edate)
    date = data.index.to_numpy()
    data.reset_index(drop=True, inplace=True)
    data["Date"] = date

    # I will now resample the data to disaggregate by week:
    weekly_resampled_data = data.set_index("Date").resample("W").ffill()
    weekly_resampled_data.head()

    # Now, I can save the data to a CSV file:
    weekly_resampled_data.to_csv("spy_data", sep=',')


