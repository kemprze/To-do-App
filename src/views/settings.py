from shared.globals import *
import flet as ft
from .main_screen import MainScreen
import sqlite3

class Settings:
    def __init__(self, page: ft.Page):
        self.current_settings = load_settings()
        self.page = page
        self.page.theme.color_scheme.background
        self.change_color_scheme_textlabel = ft.Text("Choose your color flair!", color=self.page.theme.color_scheme.on_primary)
        self.change_color_scheme = ft.Dropdown(
        width=self.page.width,
        value=self.current_settings[0][1],
        color=self.page.theme.color_scheme.on_primary,      
        bgcolor=self.page.theme.color_scheme.background,
        border_color=self.page.theme.color_scheme.on_secondary,
        on_change=self.change_theme_color,
        options=[
            ft.dropdown.Option(
                key="0",
                content=ft.Container(
                    content=ft.Text("Red", color=self.page.theme.color_scheme.on_primary),
                    bgcolor=self.page.theme.color_scheme.background,
                    padding=5
                ),
                text="Red"
            ),
            ft.dropdown.Option(
                key="1",
                content=ft.Container(
                    content=ft.Text("Blue", color=self.page.theme.color_scheme.on_primary),
                    bgcolor=self.page.theme.color_scheme.background,
                    padding=5
                ),
                text="Blue"
            ),
            ft.dropdown.Option(
                key="2",
                content=ft.Container(
                    content=ft.Text("Yellow", color=self.page.theme.color_scheme.on_primary),
                    bgcolor=self.page.theme.color_scheme.background,
                    padding=5
                ),
                text="Yellow"
            ),
            ft.dropdown.Option(
                key="3",
                content=ft.Container(
                    content=ft.Text("Green", color=self.page.theme.color_scheme.on_primary),
                    bgcolor=self.page.theme.color_scheme.background,
                    padding=5
                ),
                text="Green"
            ),
            ft.dropdown.Option(
                key="4",
                content=ft.Container(
                    content=ft.Text("Purple", color=self.page.theme.color_scheme.on_primary),
                    bgcolor=self.page.theme.color_scheme.background,
                    padding=5
                ),
                text="Purple"
            ),
            ft.dropdown.Option(
                key="5",
                content=ft.Container(
                    content=ft.Text("Pink", color=self.page.theme.color_scheme.on_primary),
                    bgcolor=self.page.theme.color_scheme.background,
                    padding=5
                ),
                text="Pink"
            ),
            ft.dropdown.Option(
                key="6",
                content=ft.Container(
                    content=ft.Text("Orange", color=self.page.theme.color_scheme.on_primary),
                    bgcolor=self.page.theme.color_scheme.background,
                    padding=5
                ),
                text="Orange"
            ),
        ]
    )


        self.change_night_mode = ft.Switch(
            label = "Night mode",
            value = False if self.current_settings[0][0] == 0 else True,
            on_change = self.enable_dark_mode,
            label_style=ft.TextStyle(color=self.page.theme.color_scheme.on_primary)
        )

        self.reset_app = [
            ft.Text("If you're encountering any problems, \n please press the button below to reset the app. \nWARNING: This will remove all your tasks and return the app \nto the factory view."),
            ft.FilledButton(
            text = ("Reset app"),
            color=self.page.theme.color_scheme.on_primary)]


    def enable_dark_mode(self, e):
        connection = sqlite3.connect("database.db")    
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE settings
            SET is_dark_mode = ?
            """, (e.control.value,))
        connection.commit()
        connection.close()
        self.update_view()

    def change_theme_color(self, e):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE settings
            SET color_theme = ?
                       """, (int(e.control.value),))
        connection.commit()
        connection.close()
        self.update_view()

    def update_view(self):
        if self.change_color_scheme.value is None:
            return

        if self.change_night_mode.value:
            self.page.theme = dark_themes[int(self.change_color_scheme.value)]
        else:
            self.page.theme = themes[int(self.change_color_scheme.value)]
        
        if self.page.views:
            view = self.page.views[-1]
            view.bgcolor = self.page.theme.color_scheme.background
            if view.controls and isinstance(view.controls[0], ft.AppBar):
                view.controls[0].title.color = self.page.theme.color_scheme.on_primary

        self.change_color_scheme.color = self.page.theme.color_scheme.on_primary
        self.change_color_scheme.bgcolor = self.page.theme.color_scheme.background
        self.change_color_scheme.border_color = self.page.theme.color_scheme.on_secondary
        self.change_color_scheme_textlabel.color = self.page.theme.color_scheme.on_primary
        self.change_night_mode.label_style.color = self.page.theme.color_scheme.on_primary

        for opt in self.change_color_scheme.options:
            if isinstance(opt.content, ft.Container):
                opt.content.bgcolor = self.page.theme.color_scheme.background
                opt.content.content.color = self.page.theme.color_scheme.on_primary
        
        if len(self.reset_app) > 0:
            self.reset_app[0].color = self.page.theme.color_scheme.on_primary
            self.reset_app[1].color = self.page.theme.color_scheme.on_primary

        self.page.update()
        
    def view(self) -> ft.View:
        return ft.View(
            route="/new_task",
            controls=[
                ft.AppBar(
                    title=ft.Text("Settings", color=self.page.theme.color_scheme.on_primary),
                    center_title=True,
                    actions=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: self.page.go("/main_screen")
                        )
                    ]
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.change_color_scheme_textlabel,
                            self.change_color_scheme,
                            self.change_night_mode
                        ]
                    ),
                    expand=True
                ),
            ],
            bgcolor = self.page.theme.color_scheme.background
        )
                                

def main(page: ft.Page):
    settings = Settings(page)



    
