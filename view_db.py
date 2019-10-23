import sqlite3
import pandas as pd

#creating a connection object that represents the database
conn = sqlite3.connect('chinook.db')
    
cur = conn.cursor()
    
#getting the column information for the artists and albums table e.g column name and data type
artists_col_infos = []
for col_info in cur.execute("PRAGMA TABLE_INFO(artists)"):
    artists_col_infos.append(col_info)
    
albums_col_infos = []
for col_info in cur.execute("PRAGMA TABLE_INFO(albums)"):
    albums_col_infos.append(col_info)

#querying the tables - artists and albums
artists_data =  cur.execute("SELECT * FROM artists").fetchall()

albums_data =  cur.execute("SELECT * FROM albums").fetchall()
conn.close()

#saving the dataframe (a representation of the database table)
artists_dataframe = pd.DataFrame(artists_data, columns=[col_name[1] for col_name in artists_col_infos])

albums_dataframe = pd.DataFrame(albums_data, columns=[col_name[1] for col_name in albums_col_infos])

print('See below the datatype of each column in the artists table')
print(artists_col_infos)
print()
print('See below the datatype of each column in the artists table')
print(albums_col_infos)
print()

print("A VIEW OF THE FIRST 5 ROWS AND LAST 5 ROWS OF THE ARTISTS TABLE")
print(artists_dataframe.head()), 
print(artists_dataframe.tail())
print()
print("\n\nA VIEW OF THE FIRST 5 ROWS AND LAST 5 ROWS OF THE ALBUMS TABLE")
print(albums_dataframe.head())
print(albums_dataframe.tail())