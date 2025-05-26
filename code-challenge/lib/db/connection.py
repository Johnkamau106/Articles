import sqlite3

def get_connection ():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = swlite3.row_factory
    name 
    return conn