# CRON job run by airflow

## Job Schedule
The data pipeline is scheduled to trigger at 20:30 daily.

## How it works

In airflow, a Directed Acyclic Graph (DAG) is required to define the workflow. DAG calls the python script that cleanses the data files, and move the output file to the respective folders.

1. data_files: 2 raw files that contains membership data  
(e.g. applications_dataset_1.csv, applications_dataset_2.csv)  
2. data_error_logs: file logs all failed applications  
(e.g. error_data_logs_<date>.csv)  
3. results: contains successful applications  
(e.g. cleansed_data_<date>.csv)

In this case, you can refer to "clean_applicant_DAG.py" created for this data pipeline.
The file is located in "docker-airflow-master > dags" folder

### Steps to run an airflow docker

**Step 1: Install docker image and run**

- Pull image from docker hub, all the components one by one, set up environment variables

On Terminal:
`docker pull apache/airflow`

- Run image of docker

On Terminal:
`docker run -d -p 80:80 apache/airflow`

**Step 2: Create a compose file and run**

On Terminal:
`docker-compose -f ./docker-compose-LocalExecutor.yml up -d`

>
-f : specify file name  
-d : tells docker to hide the logs and run the container in the background

"docker-compose" is used to define and run multi-container Docker applications, yaml file contains all the required images and configuration for our application, no need to worry about the connections between images as all will be setup automatically

**Step 3: Execute airflow docker in an interactive mode**

On Terminal:
`docker exec -it <container_id> sh -c "/entrypoint.sh /bin/bash"`

You can find the <container_id> by executing "docker ps" on Terminal

**Step 4: Use CLI or Launch Airflow UI to view DAGs**

List all the DAGs present in your DAGs directory

On Terminal:
`airflow list_dags`

URL (when run locally): http://localhost:8080/admin

### What you can do
In DAG, you can modify the parameters set for job schedule & email notification.
You can refer to the default_args set.

`'start_date': datetime(2022, 12, 8, 20, 30, tzinfo=local_tz)`

`'email': ['kchuying@gmail.com']`

`'email_on_failure': False,`

`'email_on_retry': False,`

`schedule_interval='@daily'`

### Tasks defined in DAG
There are 6 tasks defined in the workflow, as follows:

>
T1: Checks if "applications_dataset_1.csv" exists in the "data_files" folder  
T2: Checks if "applications_dataset_2.csv" exists in the "data_files" folder  
T3: Runs data cleansing logic (data_applicant_cleaner) located in dags>datacleaner3.py  
T4: Sends an email update once the job is completed.  
T5: Moves "applications_dataset_1.csv" file into "processed_files" folder  
T6: Moves "applications_dataset_2.csv" file into "processed_files" folder  

### Flow of task run
[t1,t2] >> t3 >> t4 >> [t5,t6]

Note: T1 & T2 runs in parallel, same applies for T5 & T6.
