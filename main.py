'''Universidad del valle de guatemala
Marco Jurado, Cristian Aguirre, Rodirgo Barrera'''
from Backend.backmain import BackendConn
import flet as ft
from flet import *
from Frontend.Screens.homepage import create_homepage
from Frontend.Screens.login import Login
from Frontend.Screens.signup import SignUp
import datetime

uri = "neo4j+s://1ec7fe72.databases.neo4j.io"
user = "neo4j"
password = "fJqmpIyc4lLAOb4CAOV-RlwHeQxXstncLEkkMpQcg_Q"

# instanciar backend y la conexion a Cypher.
neo = BackendConn(uri, user, password)


def main(page: Page):

    page.title = "routing app"
    height = page.height
    # login = Container(height=height, bgcolor='red')
    login = Login(page, height)
    signup = SignUp(page, height, neo)

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
