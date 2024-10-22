from flet import UserControl,  alignment, margin, Container, Column, Row, Image, Text, ElevatedButton, Checkbox, border_radius, padding
import flet as ft
from .components import input_text
import datetime


class SignUp(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.height = height
        self.backend = backend

    def build(self):
        nombre_input = input_text('Nombre', False, 155)
        apellido_input = input_text('Apellido', False, 155)
        dpi_input = input_text('DPI', False, 270)
        direccion_input = input_text('Direccion', False, 320)
        date_input = input_text('Fecha de nacimiento', False, 320)
        admin_check_box = Checkbox()

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
                                        content=nombre_input
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        content=apellido_input
                                    ),
                                ], alignment='center'),

                                Row([
                                    dpi_input,
                                    Column(alignment='center',
                                           controls=[
                                               admin_check_box,
                                               Container(
                                                   margin=margin.only(top=-20),
                                                   content=(
                                                       Text('Admin', color='white'))
                                               )
                                           ])
                                ], alignment='center'),
                                Container(
                                    alignment=alignment.center,
                                    content=direccion_input
                                ),
                                Container(
                                    alignment=alignment.center,
                                    content=date_input
                                ),
                            ]
                        ),
                        Container(
                            alignment=alignment.center,
                            margin=margin.only(top=15),
                            content=ElevatedButton(
                                on_click=lambda _:self.CrearNodo(
                                    nombre_input.value,
                                    apellido_input.value,
                                    dpi_input.value,
                                    direccion_input.value,
                                    date_input.value,
                                    admin_check_box.value
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

    def CrearNodo(self, nombre, apellido, dpi, direccion, date, admin):
        fecha = date.split("-")
        labels = ['Cliente']
        if admin:
            labels.append('Admin')
        self.backend.create_node(labels, {
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
        self.DPI = dpi
        self.page.go('/home')
