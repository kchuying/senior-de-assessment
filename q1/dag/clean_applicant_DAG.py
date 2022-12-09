from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.email_operator import EmailOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from datacleaner3 import data_applicant_cleaner
import pendulum

#Set variable yesterday_date
yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
# seven_days_ago = datetime.combine(datetime.today() - timedelta(7),
# datetime.min.time())

#Set local timezone
local_tz = pendulum.timezone("Asia/Singapore")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 12, 8, 20, 30, tzinfo=local_tz), #2022-12-8 20:30
    'email': ['kchuying@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5), #can change to minutes
}

#Create DAG (workflow) -- syntax: dag id, default_args)
#schedule_interval: DAG will run every day, week, month etc.
#catchup = TRUE means it will run historical data for period specified
#template_searchpath is the directory for mounted SQL Script folder in A/F

#using context manager to automatically assign new operators to DAG (python keyword WITH)
with DAG('clean_applicant_dag', default_args=default_args,schedule_interval='@daily', template_searchpath=['/usr/local/airflow/sql_files'], catchup=True) as dag:
#alternatively, create variable dag = DAG(...), then you need to pass variable in each operator parameters
#dag=dag parameter will assign operator to DAG

    t1 = FileSensor(
        task_id='check_file1_exists',
        filepath='/usr/local/airflow/store_files_airflow/data_files/applications_dataset_1.csv',
        fs_conn_id='fs_default',
        poke_interval=10,
        timeout=150,
        soft_fail=True
    )

    t2 = FileSensor(
        task_id='check_file2_exists',
        filepath='/usr/local/airflow/store_files_airflow/data_files/applications_dataset_2.csv',
        fs_conn_id='fs_default',
        poke_interval=10,
        timeout=150,
        soft_fail=True
    )

    t3 = PythonOperator(task_id='clean_raw_csv', python_callable=data_applicant_cleaner)

    #Send email to user, can add cc and bcc parameters
    t4 = EmailOperator(task_id='send_email_result',
        to='kchuying@gmail.com',
        subject='Daily report generated',
        html_content=""" <h1>Dataset is cleansed and ready for viewing.</h1> """,
        files=['/usr/local/airflow/store_files_airflow/results/cleansed_data_%s.csv' % yesterday_date])

    #Rename processed files and move to separate folder
    t5 = BashOperator(task_id='rename_raw_file1', bash_command='cat ~/store_files_airflow/data_files/applications_dataset_1.csv && mv ~/store_files_airflow/data_files/applications_dataset_1.csv ~/store_files_airflow/processed_files/applications_dataset_1_%s.csv' % yesterday_date)
    t6 = BashOperator(task_id='rename_raw_file2', bash_command='cat ~/store_files_airflow/data_files/applications_dataset_2.csv && mv ~/store_files_airflow/data_files/applications_dataset_2.csv ~/store_files_airflow/processed_files/applications_dataset_2_%s.csv' % yesterday_date)

    # Run task in sequence
    [t1,t2] >> t3 >> t4 >> [t5,t6]
