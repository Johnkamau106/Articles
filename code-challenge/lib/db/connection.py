import sqlite3

def get_connection():
    conn = sqlite3.connect("database.db", timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Optional: allows accessing rows like dictionaries
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn
