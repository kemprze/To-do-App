from shared.globals import *
import flet as ft
from .main_screen import MainScreen
import sqlite3

class Settings:
    def __init__(self, page: ft.Page):
        self.page = page
        self.change_color_scheme = ft.Dropdown(
            width = self.page.width,
            options = [
                ft.DropdownOption(text="Red", key="0"),
                ft.DropdownOption(text="Blue", key="1"),
                ft.DropdownOption(text="Yellow", key="2"),
                ft.DropdownOption(text="Green", key="3"),
                ft.DropdownOption(text="Purple", key="4"),
                ft.DropdownOption(text="Pink", key="5"),
                ft.DropdownOption(text="Orange", key="6")
            ],
            on_change = self.change_theme_color
        )
        self.change_night_mode = ft.Switch(
            label = "Night mode",
            value = False,
        )

        self.reset_app = [
            ft.Text("If you're encountering any problems, \n please press the button below to reset the app. \nWARNING: This will remove all your tasks and return the app \nto the factory view."),
            ft.Button(
            text = "Reset app"
            )]

    def enable_dark_mode(self):
        if self.change_night_mode.value == True:
            pass

    def change_theme_color(self, e):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE settings
            SET color_theme = ?
                       """, (int(e.control.value),))
        connection.commit()
        connection.close()

        self.page.theme = themes[int(e.control.value)]
        self.page.update()
        
    def view(self) -> ft.View:
        return ft.View(
            route="/new_task",
            controls=[
                ft.AppBar(
                    title=ft.Text(f'Settings'), 
                    center_title=True,
                    actions=[ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: self.page.go("/main_screen"))]),
                    ft.Container(content=ft.Column(controls=[ft.Text("Choose your color flair!"), self.change_color_scheme,
                                          self.change_night_mode]))
                        ])

def main(page: ft.Page):
    settings = Settings(page)



    
