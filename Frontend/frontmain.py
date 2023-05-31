import flet as ft
from flet import *
from urllib.parse import urlparse
from Screens.homepage import create_homepage
from Screens.login import Login
from Screens.signup import SignUp


def main(page: Page):
    page.title = "routing app"
    youparams = "watermelon"
    page.bgcolor = 'red'
    height = page.height
    login = Login(page, height)
    signup = SignUp(page, height)

    def route_change(route):
        # CLEAR ALL PAGE
        page.views.clear()
        page.views.append(
            View(
                route="/",
                padding=0,
                spacing=0,
                controls=[
                    login
                ],
            )
        )
        if page.route == f"/":
            page.views.clear()
            page.views.append(
                View(
                    route="/",
                    padding=0,
                    spacing=0,
                    controls=[
                        login
                    ],
                )
            )

        elif page.route == f"/signup":
            page.views.clear()
            page.views.append(
                View(
                    route="/signup",
                    padding=0,
                    spacing=0,
                    controls=[
                        signup
                    ],
                )
            )

        elif page.route == f"/home":
            page.views.clear()
            page.views.append(
                View(
                    route="/home",
                    padding=0,
                    spacing=0,
                    controls=[
                        create_homepage(page, False)
                    ],
                )
            )
    page.update()

    def view_pop():
        page.views.pop()
        myview = page.views[-1]
        page.go(myview.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main, view=ft.WEB_BROWSER)
