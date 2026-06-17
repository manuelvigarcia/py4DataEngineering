from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

url='https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
columns=['Average_rank', 'Film', 'Year']
target_file='top_50_films.csv'
target_db='Movies.db'
target_table='Top_50'

html_page = requests.get(url).text
html_tree = BeautifulSoup(html_page,"html.parser")
page_tables = html_tree.find_all("table")
#print(page_tables[0])
movies_table = None
for i,table in enumerate(page_tables):
    print(f'{i}: {table.caption}')
    if (table.caption.text.startswith('Highest Ranked Films')):
        movies_table=table
if movies_table is None:
    print('Movies table not found')
else:
    movies = movies_table.find_all('tr')
    df = pd.DataFrame(columns)
    nof_movies = 0
    for movie in movies:
        cells = movie.find_all('td')
        if len(cells)>0:  # discard the headers row
            rank = int(cells[0].text)
            film = cells[1].text
            year = int(cells[2].text)
            print(f'{rank}:{year}:{film}')
            df = pd.concat([df,pd.DataFrame([{columns[0]:rank,columns[1]:film,columns[2]:year}])],ignore_index=True)
            nof_movies=nof_movies+1
            if nof_movies>49:
                break
    df.to_csv(target_file)
    sql_connection=sqlite3.connect(target_db)
    df.to_sql(target_table,sql_connection,if_exists='replace',index=False)

