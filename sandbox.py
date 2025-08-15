import os
import sqlite3
import uuid

def load_database():
    load_database_query = """
    SELECT * FROM task
    """

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    tasks = cursor.execute(load_database_query).fetchall()
    return tasks

def initialise_database():
    create_database_query = """
        CREATE TABLE task (
        uuid SERIAL PRIMARY KEY,
        task_name TEXT NOT NULL,
        is_urgent BOOL,
        description TEXT,
        time_created DATE,
        date DATE)
    """

    dummy_task_list = [
    ("Do the laundry", True, "Do the laundry", "2024-03-25", "2025-03-25"),
    ("Write report", False, "Write report", "2024-03-25", "2025-03-25"),
    ("Feed the cat", True, "Feed the cat", "2024-03-25", "2025-03-25"),
    ("Buy groceries", False, "Buy groceries", "2024-03-25", "2025-03-25"),
    ("Exercise for 30 minutes", True, "Exercise for 30 minutes", "2024-03-25", "2025-03-25"),
    ("Call mom", False, "Call mom", "2024-03-25", "2025-03-25"),
    ("Study SQLite3", True, "Study SQLite3", "2024-03-25", "2025-03-25"),
    ("Organize desk", False, "Organize desk", "2024-03-25", "2025-03-25"),
    ("Read a book", True, "Read a book", "2024-03-25", "2025-03-25"),
    ("Pay electricity bill", False, "Pay electricity bill", "2024-03-25", "2025-03-25")
    ]

    file = open("database.db", "w")
    file.close()
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(create_database_query)

    for x in dummy_task_list:
        id = uuid.uuid4()
        cursor.execute(f"""INSERT INTO task(uuid, task_name, is_urgent, description, time_created, date)VALUES(?, ?, ?, ?, ?, ?)""", (f'{id}', x[0], x[1], x[2], x[3], x[4]))
        connection.commit()

    cursor.close()

initialise_database()