
from flet import *
from flet import border_radius, alignment, padding, margin, border_radius
import flet as ft

from components import InputText, Button


def CreateLogin(page):
    return Container(
        alignment=alignment.center,
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
                width=400,
                height=330,
                border_radius=border_radius.all(10),
                bgcolor='#1D242D',

                content=Column([
                    Container(
                        margin=margin.only(bottom=20),
                        content=Text(
                            "Bienvenido de vuelta!",
                            size=30,
                            color='#ffffff',
                            weight='bold',
                        ),
                    ),
                    Row(
                        alignment='center',
                        controls=[
                            Container(
                                alignment=alignment.center,
                                content=InputText('DPI', False, 280),
                            ),
                            Column(alignment='center',
                                   controls=[
                                       Checkbox(),
                                       Container(
                                           margin=margin.only(top=-20),
                                           content=(
                                               Text('Admin', color='white'))
                                       )
                                   ])
                        ]
                    ),
                    Container(
                        alignment=alignment.center,
                        margin=margin.only(top=15),
                        content=ElevatedButton(
                            on_click=lambda _:page.go('/home'),
                            content=Text(
                                'Iniciar Sesión',
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
                        on_click=lambda _:page.go('/signup'),
                        content=Text(
                            "Registrarse",
                            size=12,
                            color='#666C75',
                            weight='bold',
                        ),
                    ),
                ], alignment='center', horizontal_alignment='center')
            )
        ], alignment='center', horizontal_alignment='center')

    )


def CreateSignUp(page):
    return Container(
        alignment=alignment.center,
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
                                    content=InputText('Nombre', False, 155),
                                ),
                                Container(
                                    alignment=alignment.center,
                                    content=InputText('Apellido', False, 155
                                                      ),
                                ),
                            ], alignment='center'),

                            Container(
                                alignment=alignment.center,
                                content=InputText('DPI', False, 320),
                            ),
                            Container(
                                alignment=alignment.center,
                                content=InputText('Direccion', False, 320),
                            ),
                            Container(
                                alignment=alignment.center,
                                content=InputText(
                                    'Fecha de nacimiento', False, 320),
                            ),
                        ]
                    ),
                    Container(
                        alignment=alignment.center,
                        margin=margin.only(top=15),
                        content=ElevatedButton(
                            on_click=lambda _:page.go('/'),
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
                        on_click=lambda _:page.go('/signup-'),
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


def CreateTransferencia(page):

    return Container(
        expand=True,
        bgcolor='#15191E',
        content=Column(alignment='center',
                       horizontal_alignment='center',
                       controls=[
                           Container(
                               margin=margin.only(bottom=50),
                               content=Text(
                                   "TRANSFERENCIAS",
                                   size=100,
                                   color='blue',
                                   weight='bold',
                               ),
                           ),
                           Row(
                               spacing=0,
                               controls=[
                                   Container(
                                       margin=margin.only(right=100),
                                       content=Image(
                                           src='https://cdni.iconscout.com/illustration/premium/thumb/secure-money-transfer-2523253-2117429.png')
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
                                                   "Información",
                                                   size=30,
                                                   color='#ffffff',
                                                   weight='bold',
                                               ),
                                           ),
                                           Row([
                                               Container(
                                                   alignment=alignment.center,
                                                   content=InputText(
                                                       'Monto', False, 155),
                                               ),
                                               Dropdown(
                                                   width=155,
                                                   height=48,
                                                   color='grey',
                                                   bgcolor='#1D242D',
                                                   focused_bgcolor='#1D242D',
                                                   hint_text='Divisa',
                                                   hint_style=TextStyle(
                                                       color='#666C75'),
                                                   filled=False,
                                                   content_padding=padding.only(
                                                       left=15),
                                                   border_color='#666C75',
                                                   options=[
                                                       ft.dropdown.Option(
                                                           "Quetzales"),
                                                       ft.dropdown.Option(
                                                           "Dolares"),
                                                   ],
                                               )
                                           ], alignment='center'),
                                           Container(
                                               alignment=alignment.center,
                                               content=TextField(
                                                   label='No. Cuenta',
                                                   label_style=TextStyle(
                                                       color='#666C75'),
                                                   color='white',
                                                   width=320,
                                                   bgcolor='#1D242D',
                                                   filled=True,
                                                   border_color='#666C75',
                                               )
                                           ),
                                           Container(
                                               alignment=alignment.center,
                                               content=TextField(
                                                   label='Descripcion',
                                                   label_style=TextStyle(
                                                       color='#666C75'),
                                                   color='white',
                                                   width=320,
                                                   bgcolor='#1D242D',
                                                   filled=True,
                                                   border_color='#666C75',
                                                   multiline=True,
                                                   min_lines=3,
                                                   max_lines=3,
                                               )
                                           ),
                                           Container(
                                               alignment=alignment.center,
                                               margin=margin.only(top=15),
                                               content=ElevatedButton(
                                                   on_click=lambda _:page.go(
                                                       '/'),
                                                   content=Text(
                                                       'Transferir',
                                                       size=15,
                                                       weight='bold',
                                                       color="white"
                                                   ),
                                                   height=48,
                                                   width=180,
                                                   bgcolor='#0162A8'
                                               )
                                           ),
                                       ], alignment='center', horizontal_alignment='center')
                                   ),



                               ], alignment='center'
                           )])
    )


def CreateRetiro(page):

    return Container(
        expand=True,
        bgcolor='#15191E',
        content=Column(alignment='center',
                       horizontal_alignment='center',
                       controls=[
                           Container(
                               margin=margin.only(bottom=50),
                               content=Text(
                                   "RETIROS",
                                   size=100,
                                   color='blue',
                                   weight='bold',
                               ),
                           ),
                           Row(
                               spacing=0,
                               controls=[
                                   Container(
                                       margin=margin.only(right=100),
                                       content=Image(
                                           src='https://cdni.iconscout.com/illustration/premium/thumb/upi-transfer-2523250-2117426.png?f=webp')
                                   ),
                                   Container(
                                       padding=padding.only(10, 30, 10, 30),
                                       width=450,
                                       height=450,
                                       border_radius=border_radius.all(10),
                                       bgcolor='#1D242D',
                                       content=Column([
                                           Container(
                                               margin=margin.only(bottom=20),
                                               content=Text(
                                                   "Información",
                                                   size=30,
                                                   color='#ffffff',
                                                   weight='bold',
                                               ),
                                           ),
                                           Row([
                                               Container(
                                                   alignment=alignment.center,
                                                   content=InputText(
                                                       'Monto', False, 155),
                                               ),
                                               Dropdown(
                                                   width=155,
                                                   height=48,
                                                   color='grey',
                                                   bgcolor='#1D242D',
                                                   focused_bgcolor='#1D242D',
                                                   hint_text='Divisa',
                                                   hint_style=TextStyle(
                                                       color='#666C75'),
                                                   filled=False,
                                                   content_padding=padding.only(
                                                       left=15),
                                                   border_color='#666C75',
                                                   options=[
                                                       ft.dropdown.Option(
                                                           "Quetzales"),
                                                       ft.dropdown.Option(
                                                           "Dolares"),
                                                   ],
                                               )
                                           ], alignment='center'),
                                           Container(
                                               alignment=alignment.center,
                                               content=TextField(
                                                   label='Descripcion',
                                                   label_style=TextStyle(
                                                       color='#666C75'),
                                                   color='white',
                                                   width=320,
                                                   bgcolor='#1D242D',
                                                   filled=True,
                                                   border_color='#666C75',
                                                   multiline=True,
                                                   min_lines=3,
                                                   max_lines=3,
                                               )
                                           ),
                                           Container(
                                               alignment=alignment.center,
                                               margin=margin.only(top=15),
                                               content=ElevatedButton(
                                                   on_click=lambda _:page.go(
                                                       '/'),
                                                   content=Text(
                                                       'Transferir',
                                                       size=15,
                                                       weight='bold',
                                                       color="white"
                                                   ),
                                                   height=48,
                                                   width=180,
                                                   bgcolor='#0162A8'
                                               )
                                           ),
                                       ], alignment='center', horizontal_alignment='center')
                                   ),



                               ], alignment='center'
                           )])
    )
