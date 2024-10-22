from flet import UserControl,  Text, ElevatedButton, SnackBar, Container, Row, Column, ScrollMode, TextField, Dropdown, Image, padding, margin, border_radius, alignment, TextStyle
import flet as ft
from .components import input_text

# Constantes
NO_CUENTA_LABEL = 'No. Cuenta'

class ManejoCuentas(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.height = height
        self.backend = backend

    def build(self):
        # M1 - Actualizacion de motivo

        m1_no_cuenta = TextField(
            label=NO_CUENTA_LABEL,
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        m1_no_fraude = TextField(
            label='No. Fraude',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        m1_new_motivo = TextField(
            label='Nuevo motivo',
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

        # -------------------------
        m2_no_cuenta = TextField(
            label=NO_CUENTA_LABEL,
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )

        m2_banco_nuevo = Dropdown(
            width=320,
            height=48,
            color='grey',
            bgcolor='#1D242D',
            focused_bgcolor='#1D242D',
            hint_text='Banco',
            hint_style=TextStyle(
                color='#666C75'),
            filled=False,
            content_padding=padding.only(
                left=15),
            border_color='#666C75',
            options=[
                ft.dropdown.Option(
                    "BAC"),
                ft.dropdown.Option(
                    "BI"),
                ft.dropdown.Option(
                    "GYT"),
                ft.dropdown.Option(
                    "BAM"),
                ft.dropdown.Option(
                    "ANTIGUA"),
                ft.dropdown.Option(
                    "WESTERN"),
                ft.dropdown.Option(
                    "USBANK"),
            ],
        )

        # ---------------------------------
        m3_no_cuenta = TextField(
            label=NO_CUENTA_LABEL,
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        m3_no_fraude = TextField(
            label='No. Fraude',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )

        # -------------------------------
        m4dpi_1 = TextField(
            label='DPI - Persona 1',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        m4dpi_2 = TextField(
            label='DPI - Persona 2',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )

        # --------------------
        m5_no_cuenta = TextField(
            label=NO_CUENTA_LABEL,
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )

        # ----------------------------

        m6dpi_1 = TextField(
            label='DPI - Persona 1',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        m6dpi_2 = TextField(
            label='DPI - Persona 2',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        m6_tipo = Dropdown(
            width=155,
            height=48,
            color='grey',
            bgcolor='#1D242D',
            focused_bgcolor='#1D242D',
            hint_text='Tipo',
            hint_style=TextStyle(
                color='#666C75'),
            filled=False,
            content_padding=padding.only(
                left=15),
            border_color='#666C75',
            options=[
                ft.dropdown.Option(
                    "Familia"),
                ft.dropdown.Option(
                    "Amigo"),
                ft.dropdown.Option(
                    "Hermano(a)"),
                ft.dropdown.Option(
                    "Padre"),
                ft.dropdown.Option(
                    "Abuelo"),
                ft.dropdown.Option(
                    "Primo"),
                ft.dropdown.Option(
                    "Jefe"),
            ],
        )

        m6_grado = Dropdown(
            width=155,
            height=48,
            color='grey',
            bgcolor='#1D242D',
            focused_bgcolor='#1D242D',
            hint_text='Grado',
            hint_style=TextStyle(
                color='#666C75'),
            filled=False,
            content_padding=padding.only(
                left=15),
            border_color='#666C75',
            options=[
                ft.dropdown.Option(
                    "1"),
                ft.dropdown.Option(
                    "2"),
                ft.dropdown.Option(
                    "3"),
            ],
        )
        # ----------------------------

        delete_cuenta_input = TextField(
            label=NO_CUENTA_LABEL,
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )

        return Container(
            alignment=alignment.center,
            height=self.height,
            bgcolor='#15191E',
            content=Column(scroll=ScrollMode.AUTO, controls=[
                Row([
                    Container(
                        margin=margin.only(left=30, top=30, bottom=30),
                        content=Image(
                            src='https://logos-download.com/wp-content/uploads/2016/06/Yes_Bank_logo.png',
                            fit="contain",
                            width=300,
                        ),
                    ),
                    Row(
                        alignment='center',
                        controls=[
                            Container(
                                margin=margin.only(
                                    right=60, top=30, bottom=30),
                                content=delete_cuenta_input
                            ),
                            Container(
                                margin=margin.only(
                                    right=60, top=30, bottom=30),
                                content=ElevatedButton(
                                    on_click=lambda _:self.BorrarCuenta(
                                        delete_cuenta_input.value),
                                    content=Text(
                                        'Eliminar cuenta',
                                        size=15,
                                        weight='bold',
                                        color="white"
                                    ),
                                    height=48,
                                    bgcolor='red'
                                )
                            ),
                        ]
                    )
                ], vertical_alignment='center', alignment='spaceBetween'),
                Column(
                    controls=[
                        Row([
                            Container(
                                padding=padding.only(
                                    10, 30, 10, 30),
                                margin=margin.only(
                                    left=50, right=25, bottom=50),
                                expand=True,
                                height=620,
                                border_radius=border_radius.all(10),
                                bgcolor='#1D242D',
                                content=Column([
                                               Container(
                                                   margin=margin.only(
                                                       bottom=20),
                                                   content=Text(
                                                       "Actualizar motivo",
                                                       size=30,
                                                       color='#ffffff',
                                                       weight='bold',
                                                   ),
                                               ),
                                               m1_no_cuenta,
                                               m1_no_fraude,
                                               m1_new_motivo,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.ActualizarMotivo(
                                                           m1_no_cuenta.value, m1_no_fraude.value, m1_new_motivo.value),
                                                       content=Text(
                                                           'Actualizar',
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
                            Container(
                                padding=padding.only(
                                    10, 30, 10, 30),
                                margin=margin.only(
                                    left=25, right=50, bottom=50),
                                expand=True,
                                height=620,
                                border_radius=border_radius.all(10),
                                bgcolor='#1D242D',
                                content=Column([
                                               Container(
                                                   margin=margin.only(
                                                       bottom=20),
                                                   content=Text(
                                                       "Actualizar banco",
                                                       size=30,
                                                       color='#ffffff',
                                                       weight='bold',
                                                   ),
                                               ),
                                               m2_no_cuenta,
                                               m2_banco_nuevo,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.ActualizarBanco(
                                                           m2_no_cuenta.value, m2_banco_nuevo.value),
                                                       content=Text(
                                                           'Actualizar',
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
                        ], alignment='center'),
                        Row([
                            Container(
                                padding=padding.only(
                                    10, 30, 10, 30),
                                margin=margin.only(
                                    left=50, right=25, bottom=50),
                                expand=True,
                                height=620,
                                border_radius=border_radius.all(10),
                                bgcolor='#1D242D',
                                content=Column([
                                               Container(
                                                   margin=margin.only(
                                                       bottom=20),
                                                   content=Text(
                                                       "Solucionar fraude",
                                                       size=30,
                                                       color='#ffffff',
                                                       weight='bold',
                                                   ),
                                               ),
                                               m3_no_cuenta,
                                               m3_no_fraude,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.SolucionarFraude(
                                                           m3_no_cuenta.value, m3_no_fraude.value),
                                                       content=Text(
                                                           'Solucionar',
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
                            Container(
                                padding=padding.only(
                                    10, 30, 10, 30),
                                margin=margin.only(
                                    left=25, right=50, bottom=50),
                                expand=True,
                                height=620,
                                border_radius=border_radius.all(10),
                                bgcolor='#1D242D',
                                content=Column([
                                               Container(
                                                   margin=margin.only(
                                                       bottom=20),
                                                   content=Text(
                                                       "Eliminar tipo de parentezco",
                                                       size=30,
                                                       color='#ffffff',
                                                       weight='bold',
                                                   ),
                                               ),
                                               m4dpi_1,
                                               m4dpi_2,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.BorrarParentezco(
                                                           m4dpi_1.value, m4dpi_2.value),
                                                       content=Text(
                                                           'Eliminar',
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
                        ], alignment='center'),
                        Row([
                            Container(
                                padding=padding.only(
                                    10, 30, 10, 30),
                                margin=margin.only(
                                    left=50, right=25),
                                expand=True,
                                height=400,
                                border_radius=border_radius.all(10),
                                bgcolor='#1D242D',
                                content=Column([
                                               Container(
                                                   margin=margin.only(
                                                       bottom=20),
                                                   content=Text(
                                                       "Habilitar cuenta",
                                                       size=30,
                                                       color='#ffffff',
                                                       weight='bold',
                                                   ),
                                               ),
                                               m5_no_cuenta,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.ActivarCuentas(
                                                           m5_no_cuenta.value),
                                                       content=Text(
                                                           'Habilitar',
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
                            Container(
                                padding=padding.only(
                                    10, 30, 10, 30),
                                margin=margin.only(
                                    left=25, right=50),
                                expand=True,
                                height=400,
                                border_radius=border_radius.all(10),
                                bgcolor='#1D242D',
                                content=Column([
                                               Container(
                                                   margin=margin.only(
                                                       bottom=20),
                                                   content=Text(
                                                       "Crear parentezco",
                                                       size=30,
                                                       color='#ffffff',
                                                       weight='bold',
                                                   ),
                                               ),
                                               Row([
                                                   Container(
                                                       alignment=alignment.center,
                                                       content=m6_tipo
                                                   ),
                                                   Container(
                                                       alignment=alignment.center,
                                                       content=m6_grado
                                                   ),
                                               ], alignment='center'),
                                               m6dpi_1,
                                               m6dpi_2,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.CrearParentezco(
                                                           m6dpi_1.value, m6dpi_2.value, m6_tipo.value, m6_grado.value),
                                                       content=Text(
                                                           'Crear',
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

                        ], alignment='center'),

                    ]),
                Container(
                    height=200,
                ),
            ], horizontal_alignment='center')

        )

    def CrearParentezco(self, dpi1, dpi2, tipo, grado):
        try:
            self.backend.create_parentesco_relationship(
                dpi1, dpi2, tipo, grado, True)
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha creado el parentezco"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            self.page.update()
        except Exception as e:
            self.page.snack_bar = SnackBar(
                ft.Text(f"No se ha creado el parentezco"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'red'
            print(e)
            self.page.update()

    def BorrarCuenta(self, no_cuenta):
        try:
            self.backend.delete_account(no_cuenta)
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha eliminado la cuenta"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            self.page.update()
        except Exception as e:
            self.page.snack_bar = SnackBar(
                ft.Text(f"No se ha podido borrar la cuenta"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'red'
            print(e)
            self.page.update()

    def ActualizarMotivo(self, no_cuenta, no_fraude, motivo_nuevo):
        try:
            self.backend.update_involucra_motivo(
                no_cuenta, int(no_fraude), motivo_nuevo)
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha actualizado el motivo del fraude"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            self.page.update()
        except Exception as e:
            self.page.snack_bar = SnackBar(
                ft.Text(f"No se ha podido actualizar el motivo del fraude"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            print(e)
            self.page.update()

    def ActualizarBanco(self, no_cuenta, banco_nuevo):
        try:
            self.backend.update_cuenta_banco(no_cuenta, banco_nuevo)
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha actualizado el banco de la cuenta {no_cuenta}"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            self.page.update()
        except Exception as e:
            self.page.snack_bar = SnackBar(
                ft.Text(f"Ha ocurrido un error en la actualizacion del banco"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'red'
            self.page.update()
            print(e)

    def SolucionarFraude(self, no_cuenta, no_fraude):
        try:
            self.backend.delete_involucra_relationship(no_cuenta, int(no_fraude))
            self.backend.delete_fecha_alerta(int(no_fraude))
            self.backend.modificar_estado_accion_fraude(
                int(no_fraude), True, 'Resuelto')
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha solucionado el fraude {no_fraude}"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            self.page.update()
        except Exception as e:
            self.page.snack_bar = SnackBar(
                ft.Text(f"No se ha podido solucionar el fraude {no_fraude}"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'red'
            self.page.update()
            print(e)

    def BorrarParentezco(self, dpi_1, dpi_2):
        try:
            self.backend.delete_parentesco_tipo(dpi_1, dpi_2)
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha borrado el parentezco entre {dpi_1} y {dpi_2} exitosamente"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            self.page.update()
        except Exception as e:
            self.page.snack_bar = SnackBar(
                ft.Text(f"No se ha podido borrar el parentezco entre {dpi_1} y {dpi_2} exitosamente"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'red'
            self.page.update()
            print(e)

    # FALTA AGREGARLE FRONTEND
    def ActivarCuentas(self, no_cuenta):
        try:
            self.backend.activate_account(no_cuenta)
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha habilitado correctamente la cuenta {no_cuenta}"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            self.page.update()
        except Exception as e:  # Específico de Exception
            self.page.snack_bar = SnackBar(
                ft.Text(f"No se ha habilitar la cuenta {no_cuenta}")
            )
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'red'
            self.page.update()
            print(e)
