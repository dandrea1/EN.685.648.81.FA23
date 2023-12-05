# imports
import pandas as pd 
import os

# ## Data Preprocessing - FRED
# 
# https://fred.stlouisfed.org/
# 
# https://stackoverflow.com/questions/63702640/monthly-to-daily-values
# 
# Short for Federal Reserve Economic Data, FRED is an online database consisting of hundreds of thousands of economic data time series from scores of national, international, public, and private sources. We will use this data to historic information for key economic indicators in the US including, unemployment, GDP, Real GDP, Federal Funds Rate, and interest rates. All of this data can be extracted as a .csv file. 
# 
# The below code cleans this data so it can be loaded into the relational database

"""This script will update the economic data in the database if a csv file with updated data is placed in the airflow folder
"""
def previous_week_range():
    """Returns the start and end date of the previous week in MMDDYYY format."""
    today = datetime.today()
    start_of_this_week = today - timedelta(days=today.weekday())  # Monday
    end_of_last_week = start_of_this_week - timedelta(days=1)  # Sunday
    start_of_last_week = end_of_last_week - timedelta(days=6)  # Previous Monday

    return start_of_last_week.strftime('%m%d%Y'), end_of_last_week.strftime('%m%d%Y')


if __name__ == "__main__":

    gdp = "~/EN.685.648.81.FA23-main/airflow_scripts/GDPC1_raw.csv"
    real_gdp = "~/EN.685.648.81.FA23-main/airflow_scripts/GDPC1_raw.csv"
    unemployment = "~/EN.685.648.81.FA23-main/airflow_scripts/UNRATE_raw.csv"
    funds_rate = "~/EN.685.648.81.FA23-main/airflow_scripts/DFF_raw.csv"
    interest_rate = "~/EN.685.648.81.FA23-main/airflow_scripts/REAINTRATREARAT10Y_raw.csv"

    if os.path.exists(gdp):
        gdp = pd.read_csv(gdp)
        # convert to datetime
        gdp['DATE'] = pd.to_datetime(gdp['DATE'])

        # drop rows older than 1/1/2000. 
        gdp = gdp[~(gdp['DATE'] < '2000-01-01')]

        # disaggregate to week level
        gdp_cleansed = gdp.set_index('DATE').resample('W').ffill()
        gdp_cleansed.reset_index(inplace=True)

        # Real GDP is reported quarterly, in billions of dollars. The data starts 1/1/1947 and ends on 7/1/2023. First, we will convert the date to datetime. Then, we will drop rows where data is earlier than 1/1/2000. Lastly, we will disaggregate to the week level. 
    elif os.path.exists(real_gdp):
        real_gdp = pd.read_csv(real_gdp)
        # convert to datetime
        real_gdp['DATE'] = pd.to_datetime(real_gdp['DATE'])

        # drop rows older than 1/1/2000. 
        real_gdp = real_gdp[~(real_gdp['DATE'] < '2000-01-01')]

        # disaggregate to week level
        real_gdp_cleansed = real_gdp.set_index('DATE').resample('W').ffill()
        real_gdp_cleansed.reset_index(inplace=True)

    elif os.path.exists(unemployment):
        ### Unemployment Rate
        # Unemployment is reported monthly, as a percent. The data starts 1/1/1948 and ends on 10/1/2023. First, we will convert the date to datetime. Then, we will drop rows where data is earlier than 1/1/2000. Lastly, we will disaggregate to the week level. 
        unemployment = pd.read_csv(unemployment)
        # convert to datetime
        unemployment['DATE'] = pd.to_datetime(unemployment['DATE'])

        # drop rows older than 1/1/2000. 
        unemployment = unemployment[~(unemployment['DATE'] < '2000-01-01')]
        unemployment_cleansed.reset_index(inplace=True)

        # disaggregate to week level
        unemployment_cleansed = unemployment.set_index('DATE').resample('W').ffill()
    elif os.path.exists(funds_rate):
        funds_rate = pd.read_csv(funds_rate)
        # ### Federal Funds Rate
        # Federal funds rate is reported daily, as a percent. The data starts 11/16/2018 and ends on 11/12/2023. First, we will convert the date to datetime. Then, we will aggregate to the week level. 

        # convert to datetime
        funds_rate['DATE'] = pd.to_datetime(funds_rate['DATE'])

        # aggregate to week level
        funds_rate_cleansed = funds_rate.set_index('DATE').resample('W').ffill()
        funds_rate_cleansed.reset_index(inplace=True)
    elif os.path.exists(interest_rate):
        interest_rate = pd.read_csv(interest_rate)
        # ### Interest Rate 
        # Interest rate is reported monthly, as a percent. The data starts 1/1/1982 and ends on 11/1/2023. First, we will convert the date to datetime. Then, remove anything before the year 2000. Lastly, we will disaggregate to the week level.

        # convert to datetime
        interest_rate['DATE'] = pd.to_datetime(interest_rate['DATE'])

        # drop rows older than 1/1/2000. 
        interest_rate = interest_rate[~(interest_rate['DATE'] < '2000-01-01')]

        # aggregate to week level
        interest_rate_cleansed = interest_rate.set_index('DATE').resample('W').ffill()
        interest_rate_cleansed.reset_index(inplace=True)

        # Only update database if all files are present
    if os.path.exists(gdp) and os.path.exists(real_gdp) and os.path.exists(unemployment) and os.path.exists(funds_rate) and os.path.exists(interest_rate):
                
            # Ok, now we can join the data together by date, and the funds rate will have to have NaN for all thw weeks before 2018. 
            gdp_merged_df = pd.merge(gdp_cleansed, real_gdp_cleansed, on="DATE", how="inner")
            gdp__unemployment_merged_df = pd.merge(gdp_merged_df, unemployment_cleansed, on="DATE", how="inner")
            gdp__unemployment__interest_merged_df = pd.merge(gdp__unemployment_merged_df, interest_rate_cleansed, on="DATE", how="inner")
            economic_indicator_df = pd.merge(gdp__unemployment__interest_merged_df, funds_rate_cleansed, on="DATE", how="outer")
            
            # Ok, now we have 1,223 columns and six rows. Before we save to a csv, let's rename the columns and make sure the data types are correct.
            economic_indicator_df.rename(columns={"DATE":"date", "GDP":"gdp","GDPC1":"real_gdp", "UNRATE":"unemployment_rate","REAINTRATREARAT10Y":"interest_rate","DFF":"fund_rate"}, inplace=True)

            bdate, edate = previous_week_range()
            # Convert bdate and edate to datetime for comparison
            bdate = pd.to_datetime(bdate)
            edate = pd.to_datetime(edate)

            # Filter out dates that are not in the previous week
            economic_indicator_df = economic_indicator_df[(economic_indicator_df['date'] >= bdate) & (economic_indicator_df['date'] <= edate)]

            # Now, we check the datatypes. 
            # The data types looks correct. Lastly, save to a csv that can be inserted into the database. 
            economic_indicator_df.to_csv('economic_indicators', sep=',')
    else:
        print("No new updates")
