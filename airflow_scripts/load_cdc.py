import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
pd.set_option('display.max_rows', None)

"""This script will update the database if an updated cdc data file is placed in the aiflow script folder.
"""

def previous_week_range():
    """Returns the start and end date of the previous week in YYYYMMDD format."""
    today = datetime.today()
    start_of_this_week = today - timedelta(days=today.weekday())  # Monday
    end_of_last_week = start_of_this_week - timedelta(days=1)  # Sunday
    start_of_last_week = end_of_last_week - timedelta(days=6)  # Previous Monday
    return start_of_last_week.strftime('%Y-%m-%d'), end_of_last_week.strftime('%Y-%m-%d')

if __name__ == '__main__':
    bdate, edate = previous_week_range()

    # Convert bdate and edate to datetime for comparison
    bdate = pd.to_datetime(bdate)
    edate = pd.to_datetime(edate)

    path = "~/EN.685.648.81.FA23-main/airflow_scripts/COVID-19_Case_Surveillance_Public_Use_Data_groupby_death.csv"

    if os.path.exists(path):

        # Load the customer dataset from the CSV file in the 'data' folder
        df = pd.read_csv('COVID-19_Case_Surveillance_Public_Use_Data_groupby_death.csv')
        df = df[(df.death_yn == 'Yes') | (df.death_yn == 'No')]
        df["cdc_case_earliest_dt"] = pd.to_datetime(df["cdc_case_earliest_dt"])
    
        # Filter the dataframe for the previous week
        df = df[(df["cdc_case_earliest_dt"] >= bdate) & (df["cdc_case_earliest_dt"] <= edate)]

        df["year"] = df["cdc_case_earliest_dt"].dt.year
        df["month"] = df["cdc_case_earliest_dt"].dt.month
        df["year_month"] = df["cdc_case_earliest_dt"].astype(str).str[:7]
        df['week_of_year'] = df['cdc_case_earliest_dt'].dt.isocalendar().week
        df['week_range'] = df['cdc_case_earliest_dt'].dt.to_period('W-Mon').dt.start_time.dt.strftime('%Y-%m-%d') + ' to ' + df['cdc_case_earliest_dt'].dt.to_period('W-Mon').dt.end_time.dt.strftime('%Y-%m-%d')
        df.reset_index(inplace = True, drop = True)

        df.to_csv('COVID-19_Case_Surveillance_Public_clean.csv')
    else:
        print("No new updates")

