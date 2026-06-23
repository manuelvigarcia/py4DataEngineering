import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

def scrap_deeper(table_row,column_names,row_indices):
    cells = table_row.find_all('td')
    dict_row = {}
    # first element, country name
    dict_row[column_names[0]]=cells[row_indices[0]].text.strip()
    numbers=[]
    for i in range(row_indices[0],len(cells)):  ## rest of the elements
        data = cells[i].text.strip()
        if not data.startswith('—'):
            numbers.append(data)
    dict_row[column_names[-1]]=numbers[-2]
    return dict_row


def extract_country(table_row,column_names,row_indices):
    cells = table_row.find_all('td')
    dict_row={}
    if len(cells)>=8:
        for i in range(0,len(row_indices)):
            dict_row[column_names[i]]=cells[row_indices[i]].text.strip()
    else:
        dict_row = scrap_deeper(table_row,column_names,row_indices)
    return pd.DataFrame(dict_row,index=[0])

def extract(url,table_attribs,indices):
    extracted_data = pd.DataFrame(columns=table_attribs)
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')
    table = data.find_all('tbody')[2]
    rows = table.find_all('tr')[3:] #discard headers
    print(f"found {len(rows)} table rows")
    for row in rows:
        extracted_data = pd.concat([extracted_data,extract_country(row,table_attribs,indices)],ignore_index=True)
    log_progress("Data extraction complete. Initiating Transformation process.")
    return extracted_data

def transform(data,column):
    data[column] = [round(float(gdp.replace(',',''))/1000.0,2) for gdp in data[column]]
    log_progress("Data transformation complete. Initiating loading process.")
    return data.sort_values(by=column,ascending=False)

def load_to_csv(df,csv_path):
    df.to_csv(csv_path,index=False)
    log_progress("Data saved to CSV file.")

def load_to_json(df,json_path):
    df.to_json(json_path,orient='records',lines=True)
    log_progress("Data saved to JSON file.")


def load_to_db(df,sql_connection,table_name):
    df.to_sql(table_name,sql_connection,if_exists='replace',index=False)
    log_progress("Data loaded to Database as table. Running the query.")

def run_query(query_statement, sql_connection):
    query_output=pd.read_sql(query_statement,sql_connection);
    print(query_statement)
    print(query_output)
    log_progress('Process Complete.')


def log_progress(message):
    timestamp_format='%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(logfile_txt,'a') as log_file:
        log_file.write(timestamp +' : '+ message +'\n')


url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
csv_file = 'Countries_by_GDP.csv'
json_file = 'Countries_by_GDP.json'
logfile_txt = 'etl_project_log.txt'
db_table_name = 'Countries_by_GDP'
db_file = 'World_Economies.db'
db_columns=['Country','GDP_USD_billion']
tr_data_idx=[0,6]
query_string=f'SELECT * FROM {db_table_name} where {db_columns[1]}>=100'
log_progress("Preliminaries complete. Initiating ETL process.")


df = extract(url, db_columns, tr_data_idx)
df = transform(df,db_columns[1])
load_to_csv(df, csv_file)
load_to_json(df,json_file)
conn = sqlite3.connect(db_file)
log_progress("SQL Connection initiated.")
load_to_db(df,conn,db_table_name)
run_query(query_string,conn)
conn.close()
log_progress("-")
