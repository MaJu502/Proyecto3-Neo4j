import flet as ft
from flet import *
from urllib.parse import urlparse
from screens import *
from Screens.homepage import create_homepage


def main(page: Page):
    page.title = "routing app"
    youparams = "watermelon"
    page.bgcolor = 'red'

    def route_change(route):
        # CLEAR ALL PAGE
        page.views.clear()
        page.views.append(
            View(
                route="/",
                padding=0,
                spacing=0,
                controls=[
                    CreateLogin(page)
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
                        CreateLogin(page)
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
                        CreateSignUp(page)
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
