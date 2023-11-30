--Create Schema 

CREATE SCHEMA covid
    AUTHORIZATION postgres;

-- Create Tables

-- create economic indicator table
CREATE TABLE economic_indicators(
Week_Number DATE PRIMARY KEY,
gpd FLOAT(3), 
real_gdp FLOAT(3),
unemployment_rate FLOAT(1),
interest_rate FLOAT(8),
funds_rate FLOAT(2)
	);

-- create emissions data table
CREATE TABLE emissions_data(
Week_Number DATE PRIMARY KEY,
aqi FLOAT, 
arithmetic_mean FLOAT,
first_max_value FLOAT,
observation_count FLOAT,
observation_percent FLOAT
	);


-- create covid table
CREATE TABLE covid_data(
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
CREATE TABLE stock_data(
	Week_number DATE PRIMARY KEY,
	open_price FLOAT,
	high_price FLOAT,
	low_price FLOAT,
	close_price FLOAT,
	adj_close FLOAT,
	volume INT,
	);

-- COPY data into the tables

COPY economic_indicators 
FROM '/home/jhu/Downloads/economic_indicators.csv'
DELIMITER ','
CSV HEADER
NULL ''

COPY emissions_data 
FROM '/home/jhu/Downloads/emissions_data_2017_2023.csv'
DELIMITER ','
CSV HEADER
NULL 'NA'

COPY covid_data 
FROM '/home/jhu/Downloads/COVID-19_Case_Surveillance_Public_clean.csv'
DELIMITER ','
CSV HEADER
NULL 'NA'

COPY stock_data
from '/home/jhu/Downloads/spy_data.csv'
DELIMITER ','
CSV HEADER
NULL 'NA'