Download all files in this folder and move to the home directory inside class VM "~/EN.685.648.81.FA23-main"
Navigate to this folder in the terminal.

1. cd EN.685.648.81.FA23-main

--------------Create the COVID database---------------
Run the following commands one after the other:

1. psql -U jhu -d postgres
2. \i modified_covid_schema.sql
3. \copy covid.economic_indicators FROM 'economic_indicators.csv' WITH (FORMAT csv, HEADER, NULL '');
4. \copy covid.emissions_data FROM 'emissions_data_2017_2023.csv' WITH (FORMAT csv, HEADER, NULL 'NA');
5. \copy covid.covid_data FROM 'COVID-19_Case_Surveillance_Public_clean.csv' WITH (FORMAT csv, HEADER, NULL 'NA');
6. \copy covid.stock_data FROM 'spy_data.csv' WITH (FORMAT csv, HEADER, NULL 'NA');

7. ctrl + d to exit postgres
--------------If airflow is installed---------------
Move the file DAG.py inside the "EN.685.648.81.FA23-main/airflow_scripts" to the "~/airflow/dags" folder

Run the following commands:
1. conda activate airflow_env
2. pip install pandas
3. pip install yfinance
4. pip install pandas_datareader
5. pip install psycopg2-binary
6. export AIRFLOW_HOME=~/airflow
7. airflow webserver -p 8080

Open a second terminal tab
8. conda activate airflow_env
9. export AIRFLOW_HOME=~/airflow
10. airflow scheduler

Open a web browser to localhost:8080


--------------If airflow is not installed---------------
Execute the following commands one at a time, except the airflow users create can all be executed at once:

1. conda create --name airflow_env python=3.9 -y
2. conda activate airflow_env
3. pip install pandas
4. pip install yfinance
5. pip install psycopg2-binary
6. pip install pandas_datareader
7. export AIRFLOW_HOME=~/airflow
8. conda install -c conda-forge airflow
9. airflow db init
10. cd ~/airflow

Using a text editor (nano in this case), change the line in the “airflow.cfg” file where it says load_examples from True to False. This will prevent the airflow UI from loading the example DAGs. These DAG examples can be helpful, but they also make it more difficult to find the DAGs you are creating for the assignment.

11. mkdir dags
12. airflow users create \
--username admin \
--password admin \
--firstname Brandon \
--lastname Morrow \
--role Admin \
--email bmorrow5@jh.edu

Move the file DAG.py inside the "EN.685.648.81.FA23-main/airflow_scripts" to the "~/airflow/dags" folder

13. export AIRFLOW_HOME=~/airflow
14. airflow webserver -p 8080

Open a second terminal tab and run these commands:
15. conda activate airflow_env
16. export AIRFLOW_HOME=~/airflow
17. airflow scheduler

Open a web browser to localhost:8080 
Login is admin admin

--------------Run the Airflow DAG---------------
Open localhost:8080 in a web browser to view the DAG


--------------View Reports---------------
To view or download reports on the data for further processing they can be accessed via flask API at:
stock_api = http://localhost:8001/api/spy
economics_api = http://localhost:8001/api/economics
emissions_api = http://localhost:8001/api/emissions
covid_api = http://localhost:8001/api/covid
