import sqlite3

path = 'database/data2.db'

conn = sqlite3.connect(path)
conn.close()

#curSQ = conSQ.cursor()