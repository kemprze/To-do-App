from shared.globals import *
import flet as ft
import datetime
from .main_screen import MainScreen

class NewTask:
    def __init__(self, page: ft.Page):
        self.page = page
        self.task_list = load_tasks()
        self.list_container = ft.ListView(controls=[])
        self.task_name = ft.TextField(label="What do you want to do?", label_style=ft.TextStyle(color=self.page.theme.color_scheme.on_primary), border_color=self.page.theme.color_scheme.on_primary, color=self.page.theme.color_scheme.on_primary)
        self.is_urgent = ft.Switch(label="Is it urgent?", label_style=ft.TextStyle(color=self.page.theme.color_scheme.on_primary), value=False)
        self.description = ft.TextField(label="Description", label_style=ft.TextStyle(color=self.page.theme.color_scheme.on_primary), border_color=self.page.theme.color_scheme.on_primary, color=self.page.theme.color_scheme.on_primary)
        self.time_created = datetime.date.today()
        self.due_on = ft.TextField(label="When do you want to do it?", value="Pick a value", on_click=self.open_date_picker, label_style=ft.TextStyle(color=self.page.theme.color_scheme.on_primary), border_color=self.page.theme.color_scheme.on_primary, color=self.page.theme.color_scheme.on_primary)
        self.datepicker = ft.DatePicker(
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime(2199, 1, 1),
            on_change=self.change_date,
        )

    def open_date_picker(self, e):
        # self.datepicker.pick_date()
        e.control.page.open(self.datepicker)

    def change_date(self, e):
        selected = f"{self.datepicker.value}"
        self.due_on.value = selected
        self.page.update()
        e.control.page.update()

    def add_task_database(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        tasks = load_tasks()
        id = uuid.uuid4()

        cursor.execute("""
            INSERT INTO task(uuid, task_name, is_urgent, description, time_created, date) 
                       VALUES (?, ?, ?, ?, ?, ?)""", (f'{id}', self.task_name.value, self.is_urgent.value, self.description.value, self.time_created, self.due_on.value))
    
        connection.commit()
        connection.close()
        self.page.go("/main_screen")
        
    def view(self) -> ft.View:
        return ft.View(
            route="/new_task",
            controls=[
                ft.AppBar(
                    title=ft.Text(f'New task'), 
                    center_title=True,
                    bgcolor=self.page.theme.color_scheme.primary,
                    color=self.page.theme.color_scheme.on_primary,
                    actions=[
                        ft.IconButton(content=ft.Icon(name=ft.Icons.ARROW_BACK, color=self.page.theme.color_scheme.on_primary), on_click=lambda _: self.page.go("/main_screen")),
                        ft.IconButton(content=ft.Icon(name=ft.Icons.DONE, color=self.page.theme.color_scheme.on_primary), on_click=lambda _:self.add_task_database())]),
                ft.Column(controls=[self.task_name,
                                    self.is_urgent,
                                    self.description,
                                    self.due_on])
                        ],
                        bgcolor=self.page.theme.color_scheme.background)

def main(page: ft.Page):
    new_task = NewTask(page)



    
