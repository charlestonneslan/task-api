import sqlite3

# function to get a connection to a SQLite file
def get_database_connection():
    return sqlite3.connect("tasks.db")

def init_db(conn):
    command = '''CREATE TABLE IF NOT EXISTS tasks (
                 id INTEGER PRIMARY KEY,
                 title TEXT NOT NULL,
                 description TEXT,
                 done INT DEFAULT 0
    )'''
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()

def add_task(conn, title: str, description: str):
    command = "INSERT INTO tasks (title, description) VALUES (?, ?)"
    cursor = conn.cursor()
    cursor.execute(command, (title, description))
    conn.commit()
    return cursor.lastrowid

def list_tasks(conn):
    command = "SELECT * FROM tasks"
    cursor = conn.cursor()
    cursor.execute(command)
    all_tasks = cursor.fetchall()
    return all_tasks