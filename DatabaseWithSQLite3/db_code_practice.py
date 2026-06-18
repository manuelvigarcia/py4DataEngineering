import sqlite3
import pandas as pd

conn = sqlite3.connect('STAFF.db')

table_name = 'Departments'
attribute_list=['DEPT_ID','DEP_NAME','MANAGER_ID','LOC_ID']
file_path='Departments.csv'
df = pd.read_csv(file_path,names=attribute_list)
df.to_sql(table_name,conn,if_exists='replace',index=False)
print('Table is ready')

conn.close()

