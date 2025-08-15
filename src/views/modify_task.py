from shared.globals import *
import flet as ft
import datetime
import sqlite3

class ModifyTask:
    def __init__(self, page: ft.Page, task_id=None):
        self.page = page
        self.task_id = task_id

        print(self.task_id)
        self.selected_task = self.locate_task_database()
        if not self.selected_task: 
            print(f"Task with ID {self.task_id} not found.")
            self.page.go("/main_screen")
        print(self.selected_task)

        self.list_container = ft.ListView(controls=[])
        self.task_name = ft.TextField(label="Task name", value=self.selected_task[1])
        self.is_urgent = ft.Switch(label="Urgent?", value=self.selected_task[2])
        self.description = ft.TextField(label="Description", value=self.selected_task[3])
        self.time_created = self.selected_task[4]
        self.due_on = ft.TextField(label="Due date: ", value=self.selected_task[5], on_click=self.open_date_picker)

        self.datepicker = ft.DatePicker(
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime(2199, 1, 1),
            on_change=self.change_date,
        )

    def locate_task_database(self):
        print(self.task_id)
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.result = self.cursor.execute("""
        SELECT *
        FROM task
        WHERE uuid LIKE ?
        """, (self.task_id,)).fetchone()
        self.connection.close()
        return self.result
        
    def open_date_picker(self, e):
        # self.datepicker.pick_date()
        e.control.page.open(self.datepicker)

    def change_date(self, e):
        selected = f"{self.datepicker.value}"
        self.due_on.value = selected
        self.page.update()
        e.control.page.update()

    def modify_task_database(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(f"""
            UPDATE task
            SET task_name = ?,
                is_urgent = ?,    
                description = ?,
                date = ?

            WHERE uuid = ?""", (self.task_name.value, self.is_urgent.value, self.description.value, self.due_on.value, self.selected_task[0]))
    
        connection.commit()
        connection.close()
        self.page.go("/main_screen")
        
    def view(self) -> ft.View:
        return ft.View(
            route=f"/modify_task/{self.task_id}",
            controls=[
                ft.AppBar(
                    title=ft.Text(f'Modify task'), 
                    center_title=True,
                    bgcolor=ft.Colors.BLACK,
                    color=ft.Colors.WHITE,
                    actions=[ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: self.page.go("/main_screen")),
                        ft.IconButton(icon=ft.Icons.DONE, on_click=lambda _:self.modify_task_database())]),
                ft.Column(controls=[self.task_name,
                                    self.is_urgent,
                                    self.description,
                                    self.due_on])
                        ])




    
