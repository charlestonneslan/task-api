import pytest
import sqlite3
import db

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(':memory:')
    db.init_db(conn)
    yield conn
    conn.close()

