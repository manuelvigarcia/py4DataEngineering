import sqlite3
import pandas as pd

conn = sqlite3.connect('STAFF.db')

table_name = 'Departments'
attribute_list=['DEPT_ID','DEP_NAME','MANAGER_ID','LOC_ID']

sql_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(sql_statement,conn)
print(sql_statement)
print(query_output)

sql_statement = f"SELECT DEP_NAME FROM {table_name}"
query_output = pd.read_sql(sql_statement,conn)
print(sql_statement)
print(query_output)


conn.close()
