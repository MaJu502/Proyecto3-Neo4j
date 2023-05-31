'''Universidad del valle de guatemala
Marco Jurado, Cristian Aguirre, Rodirgo Barrera'''
from Backend.backmain import App
import flet as ft
from flet import *
from urllib.parse import urlparse
from Frontend.Screens.homepage import create_homepage
from Frontend.Screens.login import Login
from Frontend.Screens.signup import SignUp
import datetime


def main(page: Page):
    uri = "neo4j+s://1ec7fe72.databases.neo4j.io"
    user = "neo4j"
    password = "fJqmpIyc4lLAOb4CAOV-RlwHeQxXstncLEkkMpQcg_Q"

    # instanciar backend y la conexion a Cypher.
    app = App(uri, user, password)

    attributes1 = {
        'nombre': 'Marco',
        'apellido': 'Jurado',
        'direccion': 'ciudad',
        'DPI': 1,
        'fecha_nacimiento': datetime.date(2001, 5, 12)
    }
    t = app.create_node('Cliente', attributes1)
    print(t)

    '''
    motivos de fraude:
        - transferencia o retiro mayor a 1.5 veces el promedio 
        - transferencia o retiro con monto mayor a 100,000
        - transferencia a cuenta ligada a fraude
        - retiro de cuenta ligada a fraude
    accion o pipeline:
        -si se cumple condicion de fraude
            > no se ejecuta la transaccion
            > se bloquea la cuenta
            > se devuelve mensaje de error
        - si no cumple condicion se hace la transaccion
    '''

    page.title = "routing app"
    page.bgcolor = 'red'
    height = page.height
    login = Login(page, height)
    signup = SignUp(page, height, app)

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
