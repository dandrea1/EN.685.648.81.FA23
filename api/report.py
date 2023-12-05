# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
import json
import pandas as pd


print("Running report.py")
# %%
stock_api = "http://localhost:8001/api/spy"
economics_api = "http://localhost:8001/api/economics"
emissions_api = "http://localhost:8001/api/emissions"
covid_api = "http://localhost:8001/api/covid"

headers = {
    'Content-Type': 'application/json'
}


# %%
stocks_data = requests.get(stock_api, headers=headers).json()["data"]
stocks_df = pd.DataFrame.from_records(stocks_data)


# %%
economic_indicators_data = requests.get(economics_api, headers=headers).json()["data"]
economic_indicators_df = pd.DataFrame.from_records(economic_indicators_data)


# %%
emissions_data = requests.get(emissions_api, headers=headers).json()["data"]
emissions_df = pd.DataFrame.from_records(emissions_data)


# %%
covid_data = requests.get(covid_api, headers=headers).json()["data"]
covid_df = pd.DataFrame.from_records(covid_data)


print("ran report.py")