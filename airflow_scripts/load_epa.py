import pandas as pd
import requests
from datetime import datetime, timedelta

"""
Emissions Data Pull
The following script will pull emissions data from the Environmental Protection Agency (EPA) website. This code will call the EPA API, and will return nationwide carbon monoxide levels. The API only allows the pull of one year of data at a time so we will consolidate at the end. 
https://aqs.epa.gov/aqsweb/documents/data_api.html
To register for the API:
https://aqs.epa.gov/data/api/signup?email=myemail@example.com
"""

def fetch_data_for_state(state, param, bdate, edate):
    """A function to fetch data for a given state, date range, and parameter
    Args:
        state ([String]): A list of designated state codes
        param (String): The parameter code to fetch data for (Carbon Monoxide, Lead, Ozone, etc.)
        bdate (String): The start date to fetch data for
        edate (String): The end date to fetch data for
    Returns:
        json: The data returned by the API in json format
    """
    # Define access parameters
    base_url = "https://aqs.epa.gov/data/api/dailyData/byState"
    email = "brandonmorrow1010@gmail.com"  
    api_key = "taupehawk58"   

    # Define the API request parameters
    params = {
        "email": email,
        "key": api_key,
        "param": param,
        "bdate": bdate,
        "edate": edate,
        "state": state
    }
    # Fetch the data
    response = requests.get(base_url, params=params)
    
    # Check if the response was successful, if so return the data, if not display status code
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed for state {state}. Status code: {response.status_code}")
        print(response.text)  # Print the actual content for debugging
        return None


def clean_emissions_data(df, selected_columns):
    """Takes in an emissions dataframe and converts it to weekly data
    Args:
        df (DataFrame): Takes in an emissions dataframe
        selected_columns (list): A list of columns to keep
    Returns:
        DataFrame: Returns a weekly emissions dataframe with filtered columns
    """    
    # Convert the "date_local" column to datetime format
    df['date_local'] = pd.to_datetime(df['date_local'], format="%Y-%m-%d")

    # Group the data by "date_local" and calculate daily averages for selected columns
    grouped = df.groupby(['date_local'])[selected_columns].mean(numeric_only=True)
    daily_aggregated_df = pd.DataFrame(grouped).round(4)

    # Disaggregate to week level and reset the index to make "date_local" a regular column
    weekly_epa = daily_aggregated_df.resample('W').ffill()
    weekly_epa.reset_index(inplace=True)
    return weekly_epa

def previous_week_range():
    """Returns the start and end date of the previous week in YYYYMMDD format."""
    today = datetime.today()
    start_of_this_week = today - timedelta(days=today.weekday())  # Monday
    end_of_last_week = start_of_this_week - timedelta(days=1)  # Sunday
    start_of_last_week = end_of_last_week - timedelta(days=6)  # Previous Monday

    return start_of_last_week.strftime('%Y%m%d'), end_of_last_week.strftime('%Y%m%d')

if __name__ == "__main__":
    selected_columns = [
        'date_local', 'parameter', 'aqi', 'arithmetic_mean', 'first_max_value', 'observation_count', 
        'observation_percent'    
        ]
    param = "42101"  # Carbon Monoxide
    state_codes = [
        '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
        '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
        '41', '42', '43', '44', '45', '46', '47', '48', '49', '50'
    ] # All states

    weekly_emissions_all_years = pd.DataFrame()
    daily_emissions_all_years = pd.DataFrame()
    bdate, edate = previous_week_range()
    all_states_data = []
    for state_code in state_codes:
        data = fetch_data_for_state(state_code, param, bdate, edate)
        print(f"Fetching EPA data for state {state_code} for week {bdate} to {edate}")
        # Check if data is not null and contains key 'Data', if so then add to list of data
        if data and 'Data' in data: 
            all_states_data.extend(data['Data'])
    if all_states_data:
        df = pd.DataFrame(all_states_data) 
        daily_emissions_all_years = pd.concat([daily_emissions_all_years, df], ignore_index=True) # Add to the main dataframe
        weekly_emissions_all_years = clean_emissions_data(daily_emissions_all_years, selected_columns)
        weekly_emissions_all_years.to_csv("emissions_data.csv", index=False)
    else:
        print("No new data from EPA API")


