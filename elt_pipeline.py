import pandas as pd
import os 
import sqlite3
import schedule
import time  
import logging
import psycopg2
from sqlalchemy import create_engine

#Automation of logging begin 
logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
#print("Files in data folder:", os.listdir('data'))

def extract_data(file_path):
    data = pd.read_csv(file_path,skiprows=4)
    return data

#data = extract_data('data/electricity_access_percent.csv')
#print(data.head(5))

#Transform part begin

def transform_data(data):
    #Drop columns we don't need
    data = data.drop(columns=['Indicator Code', 'Unnamed: 62'], errors='ignore')
    #remanes the columns 
    data = data.rename(columns={
        'Country Name' : 'country',
        'Country Code' : 'country_code',
        'Indicator Name' : 'Indicator',
    })
    #To make the year from 1990 to last 
    year_columns= [str(year) for year in range(1990,2017)]
    columns_tokeep= ['country' , 'country_code']+ year_columns
    data = data[columns_tokeep]
    
    #Melt parameter to sort the values 
    data = data.melt(
        id_vars= ['country','country_code'],
        var_name='Year',
        value_name='electricity_access',
    )
    #drop empty rows from the electricity_access columns
    data = data.dropna(subset=['electricity_access'])
    #round for 2 decimal points only
    data['electricity_access']= data['electricity_access'].round(2)
    print('transformation Done',len(data))
    return data

#clean_data = transform_data(data)
#print(clean_data.head(5))

# Loading Part begins

def load_data(data):
    engine = create_engine('postgresql://postgres:saud1234@localhost:5432/etl_project')
    data.to_sql('electricity', engine, if_exists='replace', index=False)
    print('Load Done - Data in PostgreSQL!')
    logging.info('Load Done - PostgreSQL')

#load_data(clean_data)

#Orchestration begin
def orchestrated():
    try:
        logging.info("pipeline Started")
        data = extract_data('data/electricity_access_percent.csv')
        logging.info("extract Done")
        #if above fail the next never run
        transformation = transform_data(data)
        logging.info("Transformation Done")
        #if this fails
        load = load_data(transformation)
        logging.info("Loading Done ")
    except Exception as e:
        logging.error(f'Pipeline Failed at: {e}')
orchestrated()
#Scheduling begin
# Tell scheduling time
schedule.every().day.at("09:00").do(orchestrated)
# keep the program runing 
while True:
    schedule.run_pending()
    time.sleep(60)
