import db

def test_add_task(db_conn):
    db.add_task(db_conn, "Test title", "Test description")

    cursor = db_conn.cursor()
    cursor.execute("SELECT title FROM tasks WHERE title = 'Test title'")
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == "Test title"

def test_list_tasks(db_conn):
    db.add_task(db_conn, "Title 1", "Description 1")
    db.add_task(db_conn, "Title 2", "Description 2")
    
    tasks = db.list_tasks(db_conn)
    assert len(tasks) == 2
    assert tasks[0] == (1, "Title 1", "Description 1", 0)
    assert tasks[1] == (2, "Title 2", "Description 2", 0)

