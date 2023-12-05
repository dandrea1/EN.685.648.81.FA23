-- Create Schema if it does not exist

CREATE SCHEMA IF NOT EXISTS covid
    AUTHORIZATION postgres;

-- Create Tables with checks to avoid errors if they already exist

-- create economic indicator table
CREATE TABLE IF NOT EXISTS covid.economic_indicators (
    Week_Number DATE PRIMARY KEY,
    gdp FLOAT(3), 
    real_gdp FLOAT(3),
    unemployment_rate FLOAT(1),
    interest_rate FLOAT(8),
    funds_rate FLOAT(2)
);

-- create emissions data table
CREATE TABLE IF NOT EXISTS covid.emissions_data (
    Week_Number DATE PRIMARY KEY,
    aqi FLOAT, 
    arithmetic_mean FLOAT,
    first_max_value FLOAT,
    observation_count FLOAT,
    observation_percent FLOAT
);

-- create covid table
CREATE TABLE IF NOT EXISTS covid.covid_data (
    Week_Number DATE NOT NULL,
    cdc_report_dt INT, 
    death_yn VARCHAR(3) NOT NULL,
    year INT,
    month INT,
    year_month VARCHAR(50),
    week_of_year INT,
    week_range VARCHAR(100),
    PRIMARY KEY(Week_Number, death_yn)
);

-- create stock market table
CREATE TABLE IF NOT EXISTS covid.stock_data (
    Week_number DATE PRIMARY KEY,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    adj_close FLOAT,
    volume INT
);

