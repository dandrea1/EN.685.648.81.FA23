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
    cursor.execute("SELECT * FROM covid.stock_data;")
    data = cursor.fetchall()
    resp_list = []
    cursor.close()
    db_connection.close()

    for item in data:
        resp_list.append(item)
    response = {
        "data": resp_list
    }
    return jsonify(response)

@app.route("/api/emissions", methods=["GET"])
def get_emissions_data():
    db_connection = _get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM covid.emissions_data;")
    data = cursor.fetchall()
    resp_list = []
    cursor.close()
    db_connection.close()

    for item in data:
        resp_list.append(item)
    response = {
        "data": resp_list
    }
    return jsonify(response)

@app.route("/api/economics", methods=["GET"])
def get_economic_indicators():
    db_connection = _get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM covid.economic_indicators;")
    data = cursor.fetchall()
    resp_list = []
    cursor.close()
    db_connection.close()

    for item in data:
        resp_list.append(item)
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
        resp_list.append(item)
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
