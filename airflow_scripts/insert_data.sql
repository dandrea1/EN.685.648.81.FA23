-- Insert Updated data into tables
INSERT INTO covid.economic_indicators 
FROM 'economic_indicators.csv'
DELIMITER ','
CSV HEADER
NULL ''

INSERT INTO covid.emissions_data 
FROM 'emissions_data.csv'
DELIMITER ','
CSV HEADER
NULL 'NA'

INSERT INTO covid.covid_data 
FROM 'COVID-19_Case_Surveillance_Public_clean.csv'
DELIMITER ','
CSV HEADER
NULL 'NA'

INSERT INTO covid.stock_data
from 'spy_data.csv'
DELIMITER ','
CSV HEADER
NULL 'NA'