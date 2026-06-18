from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

url='https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
columns=["Film", "Year","Rotten Tomatoes' Top 100[1]"]
sort_column=columns[2]
target_file='top_50_films.csv'
target_db='Movies.db'
target_table='Top_50'
wanted_movies=50

def save_movies_data(data,csv_file,database,db_table):
    df.to_csv(csv_file)
    sql_connection=sqlite3.connect(database)
    df.to_sql(db_table,sql_connection,if_exists='replace',index=False)

def find_columns_index(table_header,column_names):
    print(f"getting header indices from <{table_header.text}> of type {type(table_header)}")
    table_column = table_header.th
    if (table_column is None):
        return None
    indices = {}
    completed = False
    idx = 0
    for i,table_column in enumerate(table_header.find_all('th')):
        print(f"Searching for headers in <{table_column}>")
        if table_column.text in column_names:
            indices[table_column.text]=i
            print(f"Found <{table_column.text}> at index {i}")
        else:
            print(f"not interested in column <{table_column.text}>")
        if (len(indices)==len(column_names)):
            break
    print(f"{indices}")
    headers = table_header.find_all('th')
    for name in column_names:
        print(f"{name}: {indices[name]} -> {headers[indices[name]].text}")
    return indices

def scrap_table_row(table_row,column_names,data_index):
    print(f"Extracting data from <{movie}> of type {type(movie)}")
    print(f"<{table_row}> has {len(table_row.text)} characters of text: {table_row.text}")
    if len(table_row.text)<2:
        return None
    cells=table_row.find_all('td')
    dict_row={}
    for i in range(0,len(column_names)):
        print(f"{column_names[i]} is at column {data_index[column_names[i]]} and its value is <{cells[data_index[column_names[i]]].text}>")
        if cells[data_index[column_names[i]]].text == 'unranked':
            print(f"do not count unranked movie.")
            return None
        dict_row[column_names[i]]=cells[data_index[column_names[i]]].text
    return pd.DataFrame(dict_row, index=[0])

html_page = requests.get(url).text
html_tree = BeautifulSoup(html_page,"html.parser")
page_tables = html_tree.find_all("table")
#print(page_tables[0])
movies_table = None
for i,table in enumerate(page_tables):
    print(f'{i}: {table.caption}')
    if (table.caption.text.startswith('Highest Ranked Films')):
        movies_table=table
        break
if movies_table is None:
    print('Movies table not found')
else:
    movies = movies_table.find_all('tr')
    print(columns)
    df = pd.DataFrame(columns=columns)
    print(df)
    header_row = movies_table.tr
    columns_index=find_columns_index(header_row,columns)
    nof_movies = 0
    movie = header_row.next_sibling
    while (movie is not None) and (nof_movies<wanted_movies):
        row_df=scrap_table_row(movie,columns,columns_index)
        if row_df is not None:
            df = pd.concat([df,row_df],ignore_index=True)
            nof_movies+=1
        else:
            print(f"row {movie.text} did not give any data")
        movie=movie.next_sibling
    print(columns)
    print(df)
    save_movies_data(df.sort_values(sort_column),target_file,target_db,target_table)
