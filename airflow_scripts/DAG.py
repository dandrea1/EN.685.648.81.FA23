import os
import json
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from airflow.utils.trigger_rule import TriggerRule


# define the default arguments
default_args = {
	'owner': 'data_engineer',
	'start_date': datetime(2023, 4, 6),
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

# define the DAG
with DAG('process_student_data', default_args=default_args, schedule_interval='@weekly') as dag:

	load_epa_task = BashOperator(
			task_id="load_epa",
			bash_command="python ~/EN.685.648.81.FA23-main/airflow_scripts/load_epa.py",
			dag=dag
		)
	load_cdc_task = BashOperator(
			task_id="load_cdc",
			bash_command="python ~/EN.685.648.81.FA23-main/airflow_scripts/load_cdc.py",
			dag=dag
		)
	load_stock_task = BashOperator(
			task_id="load_stock",
			bash_command="python ~/EN.685.648.81.FA23-main/airflow_scripts/load_stock.py",
			dag=dag
		)
	load_economic_task = BashOperator(
			task_id="load_economic",
			bash_command="python ~/EN.685.648.81.FA23-main/airflow_scripts/load_economic.py",
			dag=dag
		)
	store_data_task = BashOperator(
			task_id="store_data",
			bash_command="psql -h localhost -d postgres -U jhu -f ~/EN.685.648.81.FA23-main/airflow_scripts/insert_data.sql",
			dag=dag,
		)
	# # The following tasks will send an email if the previous task fails
	# email_failure_epa = EmailOperator(
	# 	task_id="email_failure_epa",
	# 	to="brandonmorrow1010@gmail.com",
	# 	subject="EPA Data Load Failure",
	# 	html_content="<p>The EPA data load task failed in your Airflow pipeline.</p>",
	# 	dag=dag,
	# 	trigger_rule=TriggerRule.ONE_FAILED
	# 	)

	# email_failure_cdc = EmailOperator(
	# 	task_id="email_failure_cdc",
	# 	to="brandonmorrow1010@gmail.com",
	# 	subject="CDC Data Load Failure",
	# 	html_content="<p>The CDC data load task failed in your Airflow pipeline.</p>",
	# 	dag=dag,
	# 	trigger_rule=TriggerRule.ONE_FAILED
	# 	)	

	# email_failure_stock = EmailOperator(
	# 	task_id="email_failure_stock",
	# 	to="brandonmorrow1010@gmail.com",
	# 	subject="Stock Data Load Failure",
	# 	html_content="<p>The Stock data load task failed in your Airflow pipeline.</p>",
	# 	dag=dag,
	# 	trigger_rule=TriggerRule.ONE_FAILED
	# 	)

	# email_failure_economic = EmailOperator(
	# 	task_id="email_failure_economic",
	# 	to="brandonmorrow1010@gmail.com",
	# 	subject="Economic Data Load Failure",
	# 	html_content="<p>The Economic data load task failed in your Airflow pipeline.</p>",
	# 	dag=dag,
	# 	trigger_rule=TriggerRule.ONE_FAILED
	# 	)	

	# # The following task will send an email if the previous tasks succeed
	# email_completed_task= EmailOperator(
	# 		task_id="email_completed",
	# 		to="brandonmorrow1010@gmail.com",
	# 		subject="Covid Data Updated",
	# 		html_content="""<p>Your Airflow pipeline has completed successfully, and the following database has been updated: Covid Data</p>""",
	# 		dag=dag
	# 	)
	# The following task will end the DAG if the previous tasks succeed

	end_task = DummyOperator(task_id="end",   
				trigger_rule=TriggerRule.ONE_SUCCESS,
		)

	# # The following tasks will send an email if the previous task fails
	# load_epa_task.on_failure_callback = email_failure_epa
	# load_cdc_task.on_failure_callback = email_failure_cdc
	# load_stock_task.on_failure_callback = email_failure_stock
	# load_economic_task.on_failure_callback = email_failure_economic

	# Execute loading tasks simultaneously then stores and emails completion
	[load_epa_task, load_cdc_task, load_stock_task, load_economic_task] >> store_data_task  >> end_task
	
