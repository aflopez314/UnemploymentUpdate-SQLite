##Create DB File

import sqlite3 as sql

conn = sql.connect('unemploymentDatabase.db')

conn.execute('CREATE TABLE JobsApplied (Site TEXT, Position TEXT, AppDate TEXT, Response TEXT, Interview TEXT)')

conn.close()
