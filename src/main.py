import flet as ft
from flet_route import Routing, path
from datetime import date
from shared.globals import *
from views.main_screen import MainScreen
from views.new_task import NewTask
from views.modify_task import ModifyTask
from views.settings import Settings

def modify_task_view(page, params=None, basket=None):
    print(f"ModifyTask parameters: {params}")
    return ModifyTask(page, task_id=(params or {}).get("task_id")).view()

def main(page: ft.Page):
    app_routes = [
        path(
            url = "/main_screen",
            clear = True,
            view = lambda page, params = None, basket = None: MainScreen(page).view()
        ),
        path(url = "/new_task",
             clear = True,
             view = lambda page, params = None, basket = None: NewTask(page).view()
             ),
        path(url = "/modify_task/:task_id",
            clear = True,
            view = modify_task_view
            ),
        path(url = "/settings",
            clear=True,
            view=lambda page, params = None, basket = None: Settings(page).view())
    ]

    Routing(
        page = page,
        app_routes = app_routes
    )
    
    page.go("/main_screen")


ft.app(target = main)
