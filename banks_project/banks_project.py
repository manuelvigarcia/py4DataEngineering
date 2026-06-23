import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import numpy
from datetime import datetime


url='https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'
page_columns=['Name', 'MC_USD_Billion']
table_columns=['MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
currencies=['GBP','EUR','INR']
csv_file='Largest_banks_data.csv'
db_name='Banks.db'
db_table_name='Largest_banks'
log_file='code_log.txt'
exchange_rates_file='exchange_rate.csv'
queries=[
    f'SELECT * FROM {db_table_name}',
    f'SELECT AVG({table_columns[0]}) FROM {db_table_name}',
    f'SELECT {page_columns[0]} FROM {db_table_name} LIMIT 5'
]

def log_progress(message):
    timestamp_format='%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp=now.strftime(timestamp_format)
    with open(log_file,'a') as f:
        f.write(timestamp+' : '+message+'\n')

def extract(source,columns):
    page=requests.get(source).text
    data=BeautifulSoup(page,'html.parser')
    extracted=pd.DataFrame(columns=columns)
    table=data.find_all('tbody')[0]
    rows=table.find_all('tr')
    for row in rows:
        dict={}
        cells = row.find_all('td')
        if len(cells)>2:   # skip table header
            dict[columns[0]]=cells[1].text.strip()
            dict[columns[1]]=float(cells[2].text.strip())
            extracted=pd.concat([extracted,pd.DataFrame(dict,index=[0])],ignore_index=True)
    return extracted

def transform(data,er_file):
    e_rates=pd.read_csv(er_file)
    e_rates=e_rates.set_index('Currency')['Rate']
    e_rates=e_rates.to_dict()
    for i in range(0,len(currencies)):
        data[table_columns[i]]=[round(dollars*e_rates[currencies[i]],2) for dollars in data[page_columns[1]]]
    return data

def load_to_csv(data,file):
    data.to_csv(file,index=False)

def load_to_db(data,conn,database_table):
    data.to_sql(database_table,conn,if_exists='replace',index=False)

def run_queries(statement,conn):
    print(statement)
    query_output=pd.read_sql(statement,conn)
    print(query_output)

log_progress('Preliminaries complete. Initiating ETL process')
dframe=extract(url,page_columns)
#print(dframe)
log_progress("Data extraction complete. Initiating Transformation process")
transformed=transform(dframe,exchange_rates_file)
print(transformed)
log_progress("Data transformation complete. Initiating Loading process")
print(transformed['MC_EUR_Billion'][4])
load_to_csv(transformed,csv_file)
log_progress('Data saved to CSV file')
sql_connection=sqlite3.connect(db_name)
log_progress('SQL Connection initiated')
load_to_db(transformed,sql_connection,db_table_name)
log_progress('Data loaded to Database as a table, Executing queries')
for i in range(0,len(queries)):
    run_queries(queries[i],sql_connection)
log_progress('Process Complete')
sql_connection.close()
log_progress('Server Connection closed')
