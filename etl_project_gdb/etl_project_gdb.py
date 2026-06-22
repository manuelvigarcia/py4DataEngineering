import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

def extract(url,table_attribs,indices):
    extracted_data = pd.DataFrame(columns=table_attribs)
    html_page = requests.get(url).text
    print(html_page)
    data = BeautifulSoup(html_page, 'html.parser')
    table = data.find_all('tbody')[2]
    rows = table.find_all('tr')[3:] #discard headers
    print(f"found {len(rows)} table rows")
    for row in rows:
        extracted_data = pd.concat([extracted_data,extract_country(row,table_attribs,indices)],ignore_index=True)
    return extracted_data

def scrap_deeper(table_row,column_names,row_indices):
    cells = table_row.find_all('td')
    dict_row = {}
    # first element, country name
    dict_row[column_names[0]]=cells[row_indices[0]].text.strip()
    print('\n\n')
    print('\n\n')
    print(dict_row)
    print('\n\n')
    print('\n\n')
    numbers=[]
    for i in range(row_indices[0],len(cells)):  ## rest of the elements
        data = cells[i].text.strip()
        if (not data.startswith('-')):
            numbers.append(data)
    dict_row[column_names[-1]]=numbers[-2]
    print('\n\n')
    print('\n\n')
    print(dict_row)
    print('\n\n')
    print('\n\n')
    return dict_row


def extract_country(table_row,column_names,row_indices):
    cells = table_row.find_all('td')
    dict_row={}
    for i in range(0,len(row_indices)):
        try:
            dict_row[column_names[i]]=cells[row_indices[i]].text.strip()
        except IndexError:
            print('missing data')
            dict_row = scrap_deeper(table_row,column_names,row_indices)
    log_progress(f"Found <{dict_row}>")
    return pd.DataFrame(dict_row,index=[0])

def transform(df):
    log_progress('Transforming data')
    return df

def load_to_csv(df,csv_path):
    log_progress('Writing to file')


def load_to_db(df,sql_connection,table_name):
    log_progress('Writing to database')

def run_query(query_statement, sql_connection):
    log_progress('Reading database')


def log_progress(message):
    print('>>> ' + message)
    timestamp_format='%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(logfile_txt,'a') as log_file:
        log_file.write(timestamp +','+ message +'\n')


url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
json_file = 'Countries_by_GDP.json'
logfile_txt = 'etl_project_log.txt'
db_table_name = 'Countries_by_GDP'
db_file = 'World_Economies.db'
db_columns=['Country','GDP_USD_billion']
tr_data_idx=[0,6]
query_string='entries with more than a 100 billion USD economy.'


log_progress("Fetching data.")
df = extract(url, db_columns, tr_data_idx)
print(df)

