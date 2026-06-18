import sqlite3
import pandas as pd

conn = sqlite3.connect('STAFF.db')

table_name = 'Departments'
attribute_list=['DEPT_ID','DEP_NAME','MANAGER_ID','LOC_ID']

#file_path='Departments.csv'
#df = pd.read_csv(file_path,names=attribute_list)
#df.to_sql(table_name,conn,if_exists='replace',index=False)
#print('Table is ready')

new_data_dict = {
    'DEPT_ID':[9],
    'DEP_NAME':['Quality Assurance'],
    'MANAGER_ID':[30010],
    'LOC_ID':['L0010']
    }
new_data=pd.DataFrame(new_data_dict)
new_data.to_sql(table_name,conn,if_exists='append',index=False)


conn.close()
