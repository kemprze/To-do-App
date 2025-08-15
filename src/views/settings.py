from shared.globals import *
import flet as ft
from .main_screen import MainScreen

class Settings:
    def __init__(self, page: ft.Page):
        self.page = page
        self.change_color_scheme = ft.Dropdown(
            width = 100,
            options = [
                ft.dropdown.Option("Red"),
                ft.dropdown.Option("Green"),
                ft.dropdown.Option("Blue"),
                ft.dropdown.Option("Yellow"),
                ft.dropdown.Option("Pink"),
                ft.dropdown.Option("Orange"),
            ]
        )
        self.change_night_mode = ft.Switch(
            label = "Night mode",
            value = False
        )

        self.reset_app = [
            ft.Text("If you're encountering any problems, \n please press the button below to reset the app. \nWARNING: This will remove all your tasks and return the app \nto the factory view."),
            ft.Button(
            text = "Reset app"
            )]

    def enable_dark_mode(self):
        if self.change_night_mode.value == True:
            pass
        
    def view(self) -> ft.View:
        return ft.View(
            route="/new_task",
            controls=[
                ft.AppBar(
                    title=ft.Text(f'Settings'), 
                    center_title=True,
                    bgcolor=ft.Colors.BLACK,
                    color=ft.Colors.WHITE,
                    actions=[ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: self.page.go("/main_screen"))]),
                    ft.Container(content=ft.Column(controls=[ft.Text("Choose your color flair!"), self.change_color_scheme,
                                          self.change_night_mode]))
                        ])

def main(page: ft.Page):
    new_task = Settings(page)



    
