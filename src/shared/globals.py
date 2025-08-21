from dataclasses import dataclass
import flet as ft

import sqlite3
import os
import uuid

themes = [
    ft.Theme(
    color_scheme = ft.ColorScheme(
        primary = ft.Colors.RED,
        secondary = ft.Colors.RED_300,
        background = ft.Colors.RED_50,
        surface = ft.Colors.RED_400,
        on_primary = ft.Colors.WHITE,
        on_secondary = ft.Colors.BLACK
    )
),
ft.Theme(
    color_scheme = ft.ColorScheme(
        primary = ft.Colors.BLUE,
        secondary = ft.Colors.BLUE_300,
        background = ft.Colors.BLUE_50,
        surface = ft.Colors.BLUE_400,
        on_primary = ft.Colors.WHITE,
        on_secondary = ft.Colors.BLACK
    )
),
ft.Theme(
    color_scheme = ft.ColorScheme(
        primary = ft.Colors.YELLOW,
        secondary = ft.Colors.YELLOW_300,
        background = ft.Colors.YELLOW_50,
        surface = ft.Colors.YELLOW_400,
        on_primary = ft.Colors.WHITE,
        on_secondary = ft.Colors.BLACK
    )
),
ft.Theme(
    color_scheme = ft.ColorScheme(
        primary = ft.Colors.GREEN,
        secondary = ft.Colors.GREEN_300,
        background = ft.Colors.GREEN_50,
        surface = ft.Colors.GREEN_400,
        on_primary = ft.Colors.WHITE,
        on_secondary = ft.Colors.BLACK
    )
),
ft.Theme(
    color_scheme = ft.ColorScheme(
        primary = ft.Colors.PURPLE,
        secondary = ft.Colors.PURPLE_300,
        background = ft.Colors.PURPLE_50,
        surface = ft.Colors.PURPLE_400,
        on_primary = ft.Colors.WHITE,
        on_secondary = ft.Colors.BLACK
    )
),
ft.Theme(
    color_scheme = ft.ColorScheme(
        primary = ft.Colors.PINK,
        secondary = ft.Colors.PINK_300,
        background = ft.Colors.PINK_50,
        surface = ft.Colors.PINK_400,
        on_primary = ft.Colors.WHITE,
        on_secondary = ft.Colors.BLACK
    )
),
ft.Theme(
    color_scheme = ft.ColorScheme(
        primary = ft.Colors.ORANGE,
        secondary = ft.Colors.ORANGE_300,
        background = ft.Colors.ORANGE_50,
        surface = ft.Colors.ORANGE_400,
        on_primary = ft.Colors.WHITE,
        on_secondary = ft.Colors.BLACK
    )
)]

def update_task_db(task_container):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    tasks = load_tasks()

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


def load_tasks():
    load_tasks_query = """
    SELECT * FROM task
    """

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    tasks = list(cursor.execute(load_tasks_query).fetchall())
    connection.close()
    return tasks

def load_settings():
    load_settings_query = """
    SELECT * FROM settings
    """

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    settings = list(cursor.execute(load_settings_query).fetchall())
    connection.close()
    return settings

def initialise_database():
    create_database_query = """
        CREATE TABLE task (
        uuid TEXT PRIMARY KEY,
        task_name TEXT NOT NULL,
        is_urgent BOOL,
        description TEXT,
        time_created DATE,
        date DATE)
    """

    create_setting_query = """
        CREATE TABLE settings (
            is_dark_mode BOOL,
            color_theme INT
        )
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

    dummy_settings = [
        (False, 0)
    ]

    if os.path.isfile("database.db") == False:
        print("No database found. Initializing a new one...")
        file = open("database.db", "w")
        file.close()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(create_database_query)
        cursor.execute(create_setting_query)
        cursor.execute("""INSERT INTO settings(
                       is_dark_mode, color_theme) VALUES (?, ?)""", (dummy_settings[0][0], dummy_settings[0][1]))

        for x in dummy_task_list:
            id = uuid.uuid4()
            cursor.execute("""INSERT INTO task(uuid, task_name, is_urgent, description, time_created, date)VALUES(?, ?, ?, ?, ?, ?)""", (f'{id}', x[0], x[1], x[2], x[3], x[4]))
        
        connection.commit() 
        connection.close()  

    else:
        return




