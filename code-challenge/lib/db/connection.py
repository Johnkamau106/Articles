import sqlite3

def get_connection ():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.row_factory
    
    return conn
