import sqlite3

conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v5.db')  # Connection / Creation of the DataBase
c = conn.cursor()
conn.commit()