#import libraries
import os
from os import listdir
from os.path import isfile, join
import csv
import glob
import pandas as pd
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import re
import hashlib


#Set global variables
fpath = "/Users/chuying/Documents/senior-de-assessment/q1/data_files/"
combined_df = pd.DataFrame()
error_df = pd.DataFrame()

#Set variable yesterday_date
yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

#Create a function to read multiple files within a folder
def read_csv_file(fpath):

    global combined_df #read, write global variable within a function
    global error_df

    #Lookup files in folder with specific file prefix
    folder_dir = fpath + "applications_dataset*.csv"
    csv_files = glob.glob(folder_dir, recursive=False)

    #Check if file exists
    if len(csv_files) == 0:
        print("No data files found.")

    else:
        print(str(len(csv_files)) + " data files are found. Start reading files..")

        #For each files in folder
        for fn in csv_files:
            print("File Path: ", fn)

            df = pd.read_csv(fn)
            print("No of records found: " + str(len(df)))

            # check_for_nan = df['name'].isnull().sum()
            # print("No of nulls in name column: ",check_for_nan)

            #filter and log error records with no name
            error_records = df[df.name.isnull()] #filter invalid records where name is null
            error_msg = "No name found in record."
            log_error_record(error_records, error_msg)

            valid_records = df[df.name.notnull()] #filter valid records where name is not null
            combined_df = combined_df.append(pd.DataFrame(valid_records), ignore_index=True) #ignore_index set to True for incremental binding

        return(combined_df)

#Create a function to remove salutations
def remove_keyword(df):
    salutation = ['Mr','Ms','Miss','Mrs','Dr'] #with dot
    salutation2 = ['MD','DDS','PhD'] #without dot

    keywords = r'\b(?:{})\b[^\w\s]'.format('|'.join(salutation))
    keywords2 = r'\b(?:{})\b'.format('|'.join(salutation2))

    df['name_cleaned'] = df['name'].str.replace(keywords, '', regex=True).str.strip()
    df['name_cleaned'] = df['name_cleaned'].str.replace(keywords2, '', regex=True).str.strip()

    return(df)

#Create a function to split name string into first_name and last_name
def split_name(row):
    name_list = row.split(' ')
    #print("Before Processing:" + str(name_list))
    name_length = len(name_list)

    if(name_length == 2):
        first_name = name_list[0]
        last_name = name_list[1]

    elif(name_length > 2):
        #assuming firstname contains everything except last element in list
        name_list[0:name_length-1] = [' '.join(name_list[0: name_length-1])]
        first_name = name_list[0]
        last_name = name_list[1]

    else:
        #Assuming the only name is firstname
        first_name = name_list[0]
        last_name = "Unknown"

    return(first_name, last_name)

#Create a function to calculate years between 2 date strings
def calculate_year(d1, d2):

    d1 = datetime.strptime(str(d1), "%Y-%m-%d")
    d2 = datetime.strptime(str(d2), "%Y-%m-%d")

    difference_in_years = relativedelta(d1, d2).years
    return(difference_in_years)

#Create a function to clean date_of_birth field and calculate age to see if above_18
def check_birthdate(row):
    #only deal with one type of dates (dash instead of slash)
    row = row.replace("/","-")

    #scenario 1: 02-27-1974 or 02-05-1968
    if ("-" in row[:4] and (int(row[3:5]) > 12 or int(row[0:2]) <= 12)):
        row_cleansed = datetime.strptime(row, "%m-%d-%Y")
        formatted_date = datetime.strftime(row_cleansed, "%Y-%m-%d")
        #print("Scenario 1: " + formatted_date)

    #scenario 2: 27-08-1975
    elif ("-" in row[:4] and int(row[0:2]) > 12):
        row_cleansed = datetime.strptime(row, "%d-%m-%Y")
        formatted_date = datetime.strftime(row_cleansed, "%Y-%m-%d")
        #print("Scenario 2: " + formatted_date)

    #scenario 3, just return the original format in YYYY-MM-DD
    else:
        formatted_date = row
        #print("Scenario 3: " + formatted_date)

    #adjustable, simply modify in the format of YYYY-MM-DD
    as_of_date = "2022-01-01"

    #calculate applicant age based on DOB. If more than 18, return Yes, else No.
    applicant_age = calculate_year(as_of_date, formatted_date)

    if(applicant_age >= 18):
        return (formatted_date, "Yes")
    else:
        return (formatted_date, "No")

def check_mobile(df):

    global error_df

    df['mobile_no'] = df["mobile_no"].str.replace(" ","") #remove empty spaces

    #create new column to check if mobile number is in the form of 8 digits
    df['mobile_check'] = df['mobile_no'].apply(lambda x: 'Pass' if (x.isdigit() == True and len(x) == 8) else 'Fail')

    #Log records where mobile no does not meet criteria
    error_records = df[df["mobile_check"] == 'Fail']
    error_msg = 'Mobile Number is not in 8 digits.'
    log_error_record(error_records, error_msg)

    #return valid records for further processing
    valid_records = df[df["mobile_check"] == 'Pass']
    return(valid_records)

def check_email(df):

    df['email_check'] = df['email'].apply(lambda x: 'Valid' if ("@" in x and x[-4:] in ".com.net") else 'Invalid')

    #Log records where mobile no does not meet criteria
    error_records = df[df["email_check"] == 'Invalid']
    error_msg = "Email address format is invalid."
    log_error_record(error_records, error_msg)

    #return valid records for further processing
    valid_records = df[df["email_check"] == 'Valid']
    return(valid_records)

#Create a function to generate hash based on requirement and combined with last_name
def generate_mbr_id(df):

    df['mbr_hash'] = df['formatted_dob'].apply(lambda x: hashlib.sha256(x.encode('utf-8')).hexdigest()[:6])
    df['member_id'] = df[['last_name', 'mbr_hash']].apply("".join, axis=1)
    df.drop(['mbr_hash'], axis = 1, inplace = True) #remove column that is not required

    return(df)

#Create a reusable function to log errors whenever records fail validation checks
def log_error_record(df, error_msg):

    global error_df
    print("Logging error records...")

    df['error_message'] = error_msg
    error_records = df[['name','email','date_of_birth','mobile_no', 'error_message']]

    #append error records to error_data_log
    error_df = error_df.append(pd.DataFrame(error_records), ignore_index = True)

def main():

    global error_df

    try:

        os.chdir(fpath)     # Change the current working directory
        print("Current working dir: ", os.getcwd())

        #Read all csv files in folder path
        combined_df = read_csv_file(fpath)
        print(len(combined_df))

        #Check data statistics
        #desc =  combined_df.describe()
        #print(desc)

        #Remove salutation from name column
        combined_df = remove_keyword(combined_df)

        for idx, row in combined_df.iterrows():
            #print(row.name)
            split_res = split_name(row['name_cleaned']) #returns a tuple
            combined_df.at[idx, 'first_name'] = split_res[0]
            combined_df.at[idx, 'last_name'] = split_res[1]

            #print(row.date_of_birth)
            result = check_birthdate(row['date_of_birth']) #returns a tuple
            combined_df.at[idx, 'formatted_dob'] = result[0].replace("-","") #Format birthday field as YYYYMMDD
            combined_df.at[idx, 'above_18'] = result[1]

        #Log records where applicant age is below limit
        error_records = combined_df[combined_df["above_18"] == 'No']
        error_msg = "Age is below limit. "
        log_error_record(error_records, error_msg)

        combined_df = combined_df[combined_df["above_18"] == 'Yes']

        combined_df = check_mobile(combined_df)

        combined_df = check_email(combined_df)

        combined_df = generate_mbr_id(combined_df)

        #store rejected applicants in a csv file
        error_df.to_csv('../data_error_logs/error_data_log_{date}.csv'.format(date = yesterday_date), index=False)

        #Reorder columns in requested format
        final_df = combined_df[['first_name', 'last_name', 'formatted_dob', 'above_18', 'member_id']]

        #store successful applicants in a csv file
        final_df.to_csv('../results/cleansed_data_{date}.csv'.format(date = yesterday_date), index=False)

    except FileNotFoundError:
        print("Directory: {0} does not exist".format(fpath))
    except NotADirectoryError:
        print("{0} is not a directory".format(fpath))
    except PermissionError:
        print("You do not have permissions to change to {0}".format(fpath))
    except OSError:
        print ("Can't change working directory")
    except:
        print("Error in code, please debug.")

if __name__ == '__main__':
    main()
