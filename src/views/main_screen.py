from shared.globals import *
import flet as ft
from datetime import date
from .modify_task import ModifyTask

class BottomSheet:
    def __init__(self, page: ft.Page, task_id=None, main_screen=None):
        self.page = page
        self.task_id = task_id
        self.main_screen = main_screen
        self.bs = ft.BottomSheet(
            ft.Container(
                alignment=ft.alignment.top_center,
                content=ft.Column(
                    controls=[ft.Container(content=
                        ft.Column(controls=[
                            ft.ElevatedButton(text="Remove task", on_click=self.remove_task, width = 0.33 * float(self.page.width)),
                            ft.ElevatedButton(text="Edit task", on_click=self.modify_task, width = 0.33 * float(self.page.width))],
                            width = 0.33 * float(self.page.width),
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER
                            ),
                            padding = 10,
                        )
                    ],
                ), 
                width=0.33 * float(self.page.width),
                height=0.33 * float(self.page.height) 
            ),
            bgcolor=self.page.theme.color_scheme.secondary
        )

    def modify_task(self, e: ft.ControlEvent):
        self.page.go(f"/modify_task/{self.task_id}")

    def remove_task(self, e: ft.ControlEvent):
        if self.main_screen and self.task_id:
            self.main_screen.remove_task(self.task_id)
            self.bs.open = False
            self.page.update()

class MainScreen:
    def update_task_widgets(self):
        checkbox = ft.Checkbox(
            overlay_color = self.page.theme.color_scheme.primary,
            fill_color = {
                ft.ControlState.DEFAULT: ft.Colors.WHITE},
            check_color = self.page.theme.color_scheme.primary,
            focus_color = self.page.theme.color_scheme.primary,
            border_side=ft.BorderSide(2, color=self.page.theme.color_scheme.primary))
        self.list_container.controls = []
        for item in self.task_list:
            task_id = item[0]
            task_title = item[1]
            task_date = item[3]
            task_data = [task_id, task_date, item[4]]
            current_task_widget = ft.ListTile(
                data=task_data, 
                title=ft.Text(task_title, color=self.page.theme.color_scheme.on_primary), 
                subtitle=ft.Text(task_date, color=self.page.theme.color_scheme.on_primary),
                trailing=checkbox,
                on_long_press=lambda e, tid=task_id: self.open_bottom_sheet(tid))
                                              
            self.list_container.controls.append(current_task_widget)

    def remove_task(self, task_id):
        remove_task_db(task_id) 
        for control in self.list_container.controls[:]:
            if control.data and control.data[0] == task_id:
                    self.list_container.controls.remove(control)
        self.page.update()

    def __init__(self, page: ft.Page):
        initialise_database()
        self.page = page
        setattr(self.page, "main_screen", self)
        self.task_list = load_tasks()
        self.settings = load_settings()
        print(self.settings)
        self.is_dark_mode = self.settings[0][0]
        self.list_container = ft.ListView(controls = [], expand = True)
        if self.is_dark_mode == False:
            self.page.theme = themes[self.settings[0][1]]
        else:
            self.page.theme = dark_themes[self.settings[0][1]]
        page.update()

    def open_bottom_sheet(self, task_id):
        bottom_sheet = BottomSheet(self.page, task_id=task_id, main_screen=self)
        self.page.overlay.append(bottom_sheet.bs)
        bottom_sheet.bs.open = True
        self.page.update()

    def view(self) -> ft.View:
        current_date = date.today()
        self.update_task_widgets()

        return ft.View(
            route="/main_screen",
            controls=[
                ft.AppBar(title = ft.Text(f'Hello, today is {current_date.strftime("%d/%m/%Y")}', color=self.page.theme.color_scheme.on_primary), 
                    bgcolor = self.page.theme.color_scheme.primary,
                    center_title = True,
                    actions = [
                        ft.IconButton(
                        content = ft.Icon(
                            name=ft.Icons.SETTINGS,
                            color = self.page.theme.color_scheme.on_primary),
                            on_click = lambda _: self.page.go("/settings")
                                    )
                                ]
                            ),
                ft.Container(
                    content = self.list_container,
                    bgcolor = self.page.theme.color_scheme.background,
                    height = self.page.height
                    ),
                ft.NavigationBar( 
                    bgcolor = self.page.theme.color_scheme.primary,
                    destinations = [
                            ft.NavigationBarDestination(icon = ft.Icon(name=ft.Icons.CATEGORY, color=self.page.theme.color_scheme.on_secondary), bgcolor=self.page.theme.color_scheme.secondary),
                            ft.NavigationBarDestination(icon = ft.Icon(name=ft.Icons.ALL_INCLUSIVE, color=self.page.theme.color_scheme.on_secondary), bgcolor=self.page.theme.color_scheme.secondary),
                            ft.NavigationBarDestination(icon = ft.Icon(name=ft.Icons.STAR_SHARP, color=self.page.theme.color_scheme.on_secondary), bgcolor=self.page.theme.color_scheme.secondary)
                        ],
                    indicator_color=self.page.theme.color_scheme.secondary,
                        )],
                        floating_action_button = ft.FloatingActionButton(
                             content = ft.Icon(name=ft.Icons.ADD, 
                                                color=self.page.theme.color_scheme.on_secondary),
                                                data = 0,
                                                bgcolor = self.page.theme.color_scheme.secondary,
                                                on_click = lambda _: self.page.go("/new_task"),
                                                shape = ft.RoundedRectangleBorder(radius=25)
                                                ),
                        vertical_alignment = ft.MainAxisAlignment.START,
                        horizontal_alignment= ft.CrossAxisAlignment.STRETCH,
                        padding = 0,
                        floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_FLOAT
        )

def main(page: ft.Page):
    main_screen = MainScreen(page)
    
