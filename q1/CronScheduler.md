# CRON job run by airflow

## Job Schedule
The data pipeline is scheduled to trigger at 20:30 daily.

## How it works

** Step 1: Install docker image and run **

- Pull image from docker hub, all the components one by one, set up environment variables
`docker pull apache/airflow`

- Run image of docker
`docker run -d -p 80:80 apache/airflow`

** Step 2: Create a compose file and runs **
On Terminal:
`docker-compose -f ./docker-compose-LocalExecutor.yml up -d`

-f : specify file name
-d : tells docker to hide the logs and run the container in the background

"docker-compose" is used to define and run multi-container Docker applications, yaml file contains all the required images and configuration for our application, no need to worry about the connections between images as all will be setup automatically

** Step 3: Execute airflow docker in an interactive mode  **
On Terminal:
`docker exec -it <container_id> sh -c "/entrypoint.sh /bin/bash"`

You can find the <container_id> by executing "docker ps" on Terminal

Note that a Directed Acyclic Graph (DAG) is required to define the workflow.
In this case, you can refer to "clean_applicant_DAG.py" created for this data pipeline.
The file is located in "docker-airflow-master > dags" folder

### What you can do
In DAG, you can modify the job schedule & email recipients. You can refer to the default_args set.

`'start_date': datetime(2022, 12, 8, 20, 30, tzinfo=local_tz)`
`'email': ['kchuying@gmail.com']`
`schedule_interval='@daily'`

### Tasks defined in DAG
There are 6 tasks defined in the workflow

T1: Checks if "applications_dataset_1.csv" exists in the "data_files" folder
T2: Checks if "applications_dataset_2.csv" exists in the "data_files" folder
T3: Runs data cleansing logic (data_applicant_cleaner) located in dags>datacleaner3.py
T4: Sends an email update once the job is completed.
Note: You can set "email_on_failure" and "email_on_retry" to True to receive updates of different workflow status
T5: Moves "applications_dataset_1.csv" file into "processed_files" folder
T6: Moves "applications_dataset_2.csv" file into "processed_files" folder

### Flow of task run
[t1,t2] >> t3 >> t4 >> [t5,t6]

Note: T1 & T2 runs in parallel, same applies for T5 & T6.
