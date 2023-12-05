# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

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

fig, ax = plt.subplots(1, figsize = (20, 8))
plt.plot(stocks_df["week"], stocks_df["high"])
ax.set_title("High weekly price of SPY")
ax.set_ylabel("SPY Price")
plt.tick_params(
    bottom=False,
    labelbottom=False
)
plt.savefig("stock_data.png")

fig, ax = plt.subplots(1, figsize = (20, 8))
plt.plot(economic_indicators_df["week_number"], economic_indicators_df["interest_rate"])
ax.set_title("Interest rate")
ax.set_ylabel("Rate (in percentage)")
plt.tick_params(
    bottom=False,
    labelbottom=False
)
plt.savefig("economic_data.png")

fig, ax = plt.subplots(1, figsize = (20, 8))
plt.plot(covid_df["cdc_report_dt"])
ax.set_title("Covid Cases")
ax.set_ylabel("Number of Cases")
plt.tick_params(
    bottom=False,
    labelbottom=False
)
plt.savefig("covid_data.png")

print("ran report.py")
# %%
