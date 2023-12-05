from re import L
from flask import Flask, request, jsonify
import pandas as pd
import requests
import json
import psycopg2

app = Flask(__name__)

@app.route("/api/spy", methods=["GET"])
def get_stock_data():
    db_connection = _get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM covid.stock_data where stock_data.week_number  >= '2020-01-01';")
    data = cursor.fetchall()
    resp_list = []
    cursor.close()
    db_connection.close()
    for item in data:
        week_number, open, high, low, close, adj_close, volume = item
        item_dict = {
            "week": week_number,
            "open": open,
            "high": high,
            "low": low,
            "close": close,
            "adj_close": adj_close,
            "volume": volume
        }
        resp_list.append(item_dict)
    response = {
        "data": resp_list
    }
    return jsonify(response)

@app.route("/api/emissions", methods=["GET"])
def get_emissions_data():
    db_connection = _get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM covid.emissions_data where emissions_data.week_number >= '2020-01-01';")
    data = cursor.fetchall()
    resp_list = []
    cursor.close()
    db_connection.close()

    for item in data:
        week_number, aqi, arithmetic_mean, first_max_value, observation_count, observation_percent = item
        item_dict = {
            "week_number": week_number,
            "aqi": aqi,
            "arithmetic_mean": arithmetic_mean,
            "first_max_value": first_max_value,
            "observation_count": observation_count,
            "observation_percent": observation_percent
        }
        resp_list.append(item_dict)
    response = {
        "data": resp_list
    }
    return jsonify(response)

@app.route("/api/economics", methods=["GET"])
def get_economic_indicators():
    db_connection = _get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("select * from covid.economic_indicators where economic_indicators.week_number >= '2020-01-01';")
    data = cursor.fetchall()
    resp_list = []
    cursor.close()
    db_connection.close()

    for item in data:
        week_number, gpd, real_gdp, unemployment_rate, interest_rate, funds_rate = item
        item_dict = {
            "week_number": week_number,
            "gpd": gpd,
            "real_gdp":real_gdp,
            "unemployment_rate": unemployment_rate,
            "interest_rate": interest_rate,
            "funds_rate":funds_rate
        }
        resp_list.append(item_dict)

    response = {
        "data": resp_list
    }
    return jsonify(response)

@app.route("/api/covid", methods=["GET"])
def get_covid_data():
    db_connection = _get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM covid.covid_data;")
    data = cursor.fetchall()
    resp_list = []
    cursor.close()
    db_connection.close()

    for item in data:
        week_number, cdc_report_dt, death_yn, year, month, year_month, week_of_year, week_range = item
        item_dict = {
            "week_number":week_number,
            "cdc_report_dt": cdc_report_dt,
            "death_yn":death_yn,
            "year":year,
            "month":month,
            "year_month":year_month,
            "week_of_year":week_of_year,
            "week_range": week_range
        }
        resp_list.append(item_dict)
    response = {
        "data": resp_list
    }
    return jsonify(response)

def _get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="jhu",
        user="postgres",
    )
    return conn

if __name__ == '__main__':
    port=8001
    app.run(debug=True, port=port)
