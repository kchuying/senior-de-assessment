def generate_member_details():
    #import libraries
    import os
    from os import listdir
    from os.path import isfile, join
    import csv
    import glob
    import pandas as pd
    from datetime import date, datetime, timedelta
    from dateutil.relativedelta import relativedelta

    #Set global variables
    fpath = "/usr/local/airflow/store_files_airflow/results/"

    #Set variable yesterday_date
    yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    member_validity_date = datetime.strftime(datetime.now() + timedelta(365), '%Y-%m-%d')

    #Create a function to read multiple files within a folder
    def read_csv_file(fpath):

        #Lookup files in folder with specific file prefix
        folder_dir = fpath + "cleansed_data_{date}.csv".format(date = yesterday_date)
        output_file = glob.glob(folder_dir, recursive=False)

        #Check if file exists
        if len(output_file) == 0:
            print("No data file found.")

        else:
            print("Data file is found. Start reading file..")

            #For each files in folder
            for fn in output_file:
                print("File Path: ", fn)

                df = pd.read_csv(fn)
                print("No of records found: " + str(len(df)))

            return(df)

    os.chdir(fpath)     # Change the current working directory
    print("Current working dir: ", os.getcwd())

    #Read cleansed data in folder path
    df = read_csv_file(fpath)

    #Created some fictitious data out of convenience
    df['cust_gender_code'] = 'U'
    df['cust_phone_num'] = '98765432'
    df['cust_address'] = 'some address'
    df['cust_postal_code'] = '123456'
    df['membership_validity'] = member_validity_date
    df['membership_status'] = 'Valid'

    #Reorder columns for inputs to q2
    cust_df = df[['member_id', 'first_name', 'last_name', 'formatted_dob',
                'cust_gender_code', 'cust_phone_num', 'cust_address', 'cust_postal_code']]

    member_df = df[['member_id', 'membership_validity', 'membership_status' ]]

    #rename columns
    cust_df = cust_df.rename(columns={'member_id': 'cust_membership_id', 'first_name': 'cust_first_name',
                                            'last_name' : 'cust_last_name', 'formatted_dob': 'cust_birth_date'})

    member_df = member_df.rename(columns={'member_id': 'membership_id'})

    #write to files for loading into psql
    cust_df.to_csv('/usr/local/airflow/store_files_airflow/sql_data_files/customer.csv', index=False)
    member_df.to_csv('/usr/local/airflow/store_files_airflow/sql_data_files/membership.csv', index=False)
