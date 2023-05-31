from flet import *
import flet as ft
from .components import InputText, Button
import datetime


class SignUp(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.height = height
        self.backend = backend

    def build(self):
        nombreInput = InputText('Nombre', False, 155)
        apellidoInput = InputText('Apellido', False, 155)
        dpiInput = InputText('DPI', False, 320)
        direccionInput = InputText('Direccion', False, 320)
        dateInput = InputText('Fecha de nacimiento', False, 320)

        return Container(
            alignment=alignment.center,
            height=self.height,
            expand=True,
            bgcolor='#15191E',
            content=Column([
                Image(
                    src='https://logos-download.com/wp-content/uploads/2016/06/Yes_Bank_logo.png',
                    fit="contain",
                    width=450,
                ),
                Container(
                    padding=padding.only(10, 30, 10, 30),
                    width=450,
                    height=500,
                    border_radius=border_radius.all(10),
                    bgcolor='#1D242D',

                    content=Column([
                        Container(
                            margin=margin.only(bottom=20),
                            content=Text(
                                "Bienvenido!",
                                size=30,
                                color='#ffffff',
                                weight='bold',
                            ),
                        ),
                        Column(
                            alignment='center',
                            controls=[
                                Row([
                                    Container(
                                        alignment=alignment.center,
                                        content=nombreInput
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        content=apellidoInput
                                    ),
                                ], alignment='center'),

                                Container(
                                    alignment=alignment.center,
                                    content=dpiInput
                                ),
                                Container(
                                    alignment=alignment.center,
                                    content=direccionInput
                                ),
                                Container(
                                    alignment=alignment.center,
                                    content=dateInput
                                ),
                            ]
                        ),
                        Container(
                            alignment=alignment.center,
                            margin=margin.only(top=15),
                            content=ElevatedButton(
                                on_click=lambda _:self.CrearNodo(
                                    nombreInput.value,
                                    apellidoInput.value,
                                    dpiInput.value,
                                    direccionInput.value,
                                    dateInput.value
                                ),
                                content=Text(
                                    'Registrarse',
                                    size=15,
                                    weight='bold',
                                    color="white"
                                ),
                                height=48,
                                width=180,
                                bgcolor='#0162A8'
                            )
                        ),
                        Container(
                            margin=margin.only(bottom=20),
                            on_click=lambda _: self.page.go('/'),
                            content=Text(
                                "Iniciar sesión",
                                size=12,
                                color='#666C75',
                                weight='bold',
                            ),
                        ),
                    ], alignment='center', horizontal_alignment='center')
                )
            ], alignment='center', horizontal_alignment='center')

        )

    def CrearNodo(self, nombre, apellido, dpi, direccion, date):
        fecha = date.split("-")
        self.backend.create_node(['Cliente'], {
            'nombre': nombre,
            'apellido': apellido,
            'direccion': direccion,
            'DPI': dpi,
            'fecha_nacimiento': datetime.date(
                int(fecha[0]),
                int(fecha[1]),
                int(fecha[2])
            )
        })

    def obtener_numeros_fecha(self, cadena_fecha):
        partes = cadena_fecha.split("-")
        anio = int(partes[0])
        mes = int(partes[1])
        dia = int(partes[2])
        return anio, mes, dia

    def obtener_ano(self, cadena_fecha):
        partes = cadena_fecha.split("-")
        anio = int(partes[0])
        return anio

    def obtener_me(self, cadena_fecha):
        partes = cadena_fecha.split("-")
        anio = int(partes[0])
        return anio

    def obtener_ano(self, cadena_fecha):
        partes = cadena_fecha.split("-")
        anio = int(partes[0])
        return anio
