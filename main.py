'''Universidad del valle de guatemala
Marco Jurado, Cristian Aguirre, Rodirgo Barrera'''

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

from Backend.backmain import BackendConn
import flet as ft
from flet import Page, View
from Frontend.Screens.homepage import create_homepage
from Frontend.Screens.login import Login
from Frontend.Screens.signup import SignUp
from dotenv import load_dotenv
import os

load_dotenv()

# Obtener los valores de las credenciales desde las variables de entorno
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')

# instanciar backend y la conexion a Cypher.
neo = BackendConn(uri, user, password)
dpi = None


def main(page: Page):

    page.title = "routing app"
    height = page.height
    login = Login(page, height, neo)
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
                        create_homepage(page, neo, login.admin)
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
