import flet as ft
from flet import  Page, View
from urllib.parse import urlparse
from Frontend.Screens.homepage import create_homepage
from Frontend.Screens.login import Login
from Frontend.Screens.signup import SignUp


def main(page: Page):
    page.title = "routing app"
    page.bgcolor = 'red'
    height = page.height
    login = Login(page, height)
    signup = SignUp(page, height)

    # Function to create and add a view
    def add_view(route, control):
        page.views.clear()
        page.views.append(
            View(
                route=route,
                padding=0,
                spacing=0,
                controls=[control],
            )
        )

    def route_change(route):
        if page.route == f"/":
            add_view("/", login)

        elif page.route == f"/signup":
            add_view("/signup", signup)

        elif page.route == f"/home":
            add_view("/home", create_homepage(page, False))

        page.update()

    def view_pop():
        page.views.pop()
        myview = page.views[-1]
        page.go(myview.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER)
