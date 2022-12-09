#Import libraries
import os
import requests
import json
import pandas as pd
from datetime import datetime

#Set file path
fpath = "/Users/chuying/Documents/senior-de-assessment/q4/"

#Input start_date and end_date of analysis
start_date = "2021-01-01T00:00:00Z"
end_date = "2022-12-31T00:00:00Z"

#Define endpoint
URL = "https://api.covid19api.com/country/singapore/status/confirmed?from={}&to={}".format(start_date, end_date)

#Read data from endpoint into a dataframe
def read_json(endpoint):
    response = requests.get(URL)
    if response.status_code == 200: #200 means okay
        json_data = json.loads(response.content.decode('utf-8'))
        #print(json_data)
        #print(type(data)) #returns a list
        df = pd.DataFrame.from_dict(json_data, orient='columns') #convert list to df
        df.columns = [x.lower() for x in df.columns] #set column headers to lowercase
    return(df)


#Get daily increase/decrease value for specific columns
def get_daily_difference(df):

    prev_col_name = "prev_day_confirmed"
    diff_col_name = "daily_confirmed"

    df[prev_col_name] = df['cases'].shift().astype('Int64')
    df[diff_col_name] = df['cases'] - df[prev_col_name]

    return(df)

def split_datetime(new_df):

    #Convert datetime to date
    new_df['date'] = pd.to_datetime(new_df['date']).dt.date

    new_df.insert(0,'year',pd.DatetimeIndex(new_df['date']).year)
    new_df.insert(1,'month',pd.DatetimeIndex(new_df['date']).month)
    new_df.insert(2,'day',pd.DatetimeIndex(new_df['date']).day)

    return(new_df)

def main():

    try:

        os.chdir(fpath)     # Change the current working directory
        print("Current working dir: ", os.getcwd())

        read_df = read_json(URL)
        # print(read_df.dtypes)
        # print(read_df.columns)
        print(df['country'].unique())
        print(df['status'].unique())

        #Calculate daily difference for each variable
        read_df = get_daily_difference(read_df)

        #drop first row with no previous day value
        read_df.dropna(subset = ["prev_day_confirmed"], inplace=True)

        #split datetime into ymd
        final_df = split_datetime(read_df)
        print(final_df.columns)

        #rename_columns
        final_df = final_df.rename(columns={'cases': 'total_confirmed_cases'})

        #rearrange columns
        final_df = final_df[['date','year','month','day', 'total_confirmed_cases',
                            'prev_day_confirmed','daily_confirmed',
                            ]]
        print(final_df)

        final_df.to_csv('cleansed_covid_data.csv', index=False)

    except:
        print("Error in code, please debug.")

if __name__ == '__main__':
    main()

# Direct read data from json file
# with open('/Users/chuying/Documents/dataeng_assessment/q4/response.json') as json_file:
#     data = json.load(json_file)
# print(data)
