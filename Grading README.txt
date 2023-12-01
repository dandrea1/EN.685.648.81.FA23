Download all files in this folder and move to home directory inside class VM "~/EN.685.648.81.FA23-main"
Navigate to this folder in the terminal.

cd EN.685.648.81.FA23-main

--------------Create the COVID database---------------
Run the following commands one after the other:

1. psql -U jhu -d postgres
2. \i modified_covid_schema.sql
3. \copy covid.economic_indicators FROM 'economic_indicators.csv' WITH (FORMAT csv, HEADER, NULL '');
4. \copy covid.emissions_datSELa FROM 'emissions_data_2017_2023.csv' WITH (FORMAT csv, HEADER, NULL 'NA');
5. \copy covid.covid_data FROM 'COVID-19_Case_Surveillance_Public_clean.csv' WITH (FORMAT csv, HEADER, NULL 'NA');
6. \copy covid.stock_data FROM 'spy_data.csv' WITH (FORMAT csv, HEADER, NULL 'NA');


--------------If airflow is installed---------------
Run the following commands:
1. conda activate airflow_env
2. pip install pandas
3. pip install yfinance
4. pip install pandas_datareader
5. export AIRFLOW_HOME=~/airflow
6. airflow webserver -p 8080

Open a second terminal tab
7. conda activate airflow_env
8. export AIRFLOW_HOME=~/airflow
9. airflow scheduler

Open a web browser to localhost:8080


--------------If airflow is not installed---------------
Execute the following commands one at a time, except the airflow users create can all be executed at once:

1. conda create --name airflow_env python=3.9 -y
2. conda activate airflow_env
3. pip install pandas
4. pip install yfinance
5. pip install pandas_datareader
6. export AIRFLOW_HOME=~/airflow
7. conda install -c conda-forge airflow
8. airflow db init
9. cd airflow

Using a text editor (nano in this case), change the line in the “airflow.cfg” file where it says load_examples from True to False. This will prevent the airflow UI from loading the example DAGs. These DAG examples can be helpful, but they also make it more difficult to find the DAGs you are creating for the assignment.

10. mkdir dags
11. airflow users create \
--username admin \
--password admin \
--firstname Brandon \
--lastname Morrow \
--role Admin \
--email bmorrow5@jh.edu

12. export AIRFLOW_HOME=~/airflow
13. airflow webserver -p 8080

Open a second terminal tab and run these commands:
14. conda activate airflow_env
15. export AIRFLOW_HOME=~/airflow
16. airflow scheduler

Open a web browser to localhost:8080 
Login is admin admin

--------------Run the Airflow DAG---------------
Move the file DAG.py inside the "EN.685.648.81.FA23-main/airflow_scripts" to the "~/airflow/dags" folder
