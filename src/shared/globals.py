from dataclasses import dataclass
import flet as ft

import sqlite3
import os
import uuid

@dataclass
class Task:
    task_name: str
    priority: int
    description: str
    time_created: str
    date: int
    is_urgent: bool

    def new_task_container(self, task_name, description, time_created, date, is_urgent, priority=0):
        text = ft.Text(task_name)
        def on_checkbox_click(e):
            setattr(text, "decoration", ft.TextDecoration.LINE_THROUGH if e.control.value else ft.TextDecoration.NONE)
            text.update()

        return ft.Row(controls=[
            text,
            ft.Checkbox(value=False, 
                        on_change=on_checkbox_click)])

def update_task_db(task_container):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    tasks = load_database()

    for item in task_container.controls:
        if item not in tasks:
            cursor.execute("""
    INSERT INTO task(uuid, task_name, is_urgent, description, time_created, date) VALUES (?, ?, ?, ?, ?, ?)""", (f'{id}', item[0], item[1], item[2], item[3], item[4]))
    
    connection.commit()
    
def remove_task_db(uuid):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
                   DELETE FROM task
                   WHERE uuid = ?""", (uuid,))
    
    connection.commit()


def load_database():
    load_database_query = """
    SELECT * FROM task
    """

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    tasks = list(cursor.execute(load_database_query).fetchall())
    connection.close()
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
    ("Do the laundry", True, "Do the laundry", "20-03-2024", "25-03-2025"),
    ("Write report", False, "Write report", "20-03-2024", "25-03-2025"),
    ("Feed the cat", True, "Feed the cat", "20-03-2024", "25-03-2025"),
    ("Buy groceries", False, "Buy groceries", "20-03-2024", "25-03-2025"),
    ("Exercise for 30 minutes", True, "Exercise for 30 minutes", "20-03-2024", "25-03-2025"),
    ("Call mom", False, "Call mom", "20-03-2024", "25-03-2025"),
    ("Study SQLite3", True, "Study SQLite3", "20-03-2024", "25-03-2025"),
    ("Organize desk", False, "Organize desk", "20-03-2024", "25-03-2025"),
    ("Read a book", True, "Read a book", "20-03-2024", "25-03-2025"),
    ("Pay electricity bill", False, "Pay electricity bill", "20-03-2024", "25-03-2025")
    ]

    if os.path.isfile("database.db") == False:
        print("No database found. Initializing a new one...")
        file = open("database.db", "w")
        file.close()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(create_database_query)

        for x in dummy_task_list:
            id = uuid.uuid4()
            cursor.execute("""INSERT INTO task(uuid, task_name, is_urgent, description, time_created, date)VALUES(?, ?, ?, ?, ?, ?)""", (f'{id}', x[0], x[1], x[2], x[3], x[4]))
        
        connection.commit()    

    else:
        return




