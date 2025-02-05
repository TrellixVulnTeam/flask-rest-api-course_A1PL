import sqlite3

connection = sqlite3.connect('data.db')
# sqlite uses only one file instead of folders like SQL, SQLalchemy 
# Hence, it is a little slower than it's professional counterparts

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES(?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'Rolf', 'asdf'),
    (3, 'Bob', 'asf')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row) 

connection.commit()

connection.close()