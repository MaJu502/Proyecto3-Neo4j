from flet import *
import flet as ft
from .components import InputText, Button


class ManejoCuentas(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.height = height
        self.backend = backend

    def build(self):
        dpiInput = InputText('DPI', False, 280)

        # M1 - Actualizacion de motivo

        M1NoCuenta = TextField(
            label='No. Cuenta',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        M1NoFraude = TextField(
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
        M1NewMotivo = TextField(
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
        M2NoCuenta = TextField(
            label='No. Cuenta',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )

        M2BancoNuevo = Dropdown(
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
        M3NoCuenta = TextField(
            label='No. Cuenta',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        M3NoFraude = TextField(
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
        M4DPI1 = TextField(
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
        M4DPI2 = TextField(
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
        M5NoCuenta = TextField(
            label='No. Cuenta',
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

        M6DPI1 = TextField(
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
        M6DPI2 = TextField(
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
        M6Tipo = Dropdown(
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

        M6Grado = Dropdown(
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

        DeleteCuentaInput = TextField(
            label='No. Cuenta',
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
                                content=DeleteCuentaInput
                            ),
                            Container(
                                margin=margin.only(
                                    right=60, top=30, bottom=30),
                                content=ElevatedButton(
                                    on_click=lambda _:self.BorrarCuenta(
                                        DeleteCuentaInput.value),
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
                                               M1NoCuenta,
                                               M1NoFraude,
                                               M1NewMotivo,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.ActualizarMotivo(
                                                           M1NoCuenta.value, M1NoFraude.value, M1NewMotivo.value),
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
                                               M2NoCuenta,
                                               M2BancoNuevo,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.ActualizarBanco(
                                                           M2NoCuenta.value, M2BancoNuevo.value),
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
                                               M3NoCuenta,
                                               M3NoFraude,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.SolucionarFraude(
                                                           M3NoCuenta.value, M3NoFraude.value),
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
                                               M4DPI1,
                                               M4DPI2,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.BorrarParentezco(
                                                           M4DPI1.value, M4DPI2.value),
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
                                               M5NoCuenta,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.ActivarCuentas(
                                                           M5NoCuenta.value),
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
                                                       content=M6Tipo
                                                   ),
                                                   Container(
                                                       alignment=alignment.center,
                                                       content=M6Grado
                                                   ),
                                               ], alignment='center'),
                                               M6DPI1,
                                               M6DPI2,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.CrearParentezco(
                                                           M6DPI1.value, M6DPI2.value, M6Tipo.value, M6Grado.value),
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

    def BorrarCuenta(self, NoCuenta):
        try:
            self.backend.delete_account(NoCuenta)
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

    def ActualizarMotivo(self, NoCuenta, NoFraude, motivoNuevo):
        try:
            self.backend.update_involucra_motivo(
                NoCuenta, int(NoFraude), motivoNuevo)
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
            self.page.update()

    def ActualizarBanco(self, NoCuenta, BancoNuevo):
        try:
            self.backend.update_cuenta_banco(NoCuenta, BancoNuevo)
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha actualizado el banco de la cuenta {NoCuenta}"))
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

    def SolucionarFraude(self, NoCuenta, NoFraude):
        try:
            self.backend.delete_involucra_relationship(NoCuenta, int(NoFraude))
            self.backend.delete_fecha_alerta(int(NoFraude))
            self.backend.modificar_estado_accion_fraude(
                int(NoFraude), True, 'Resuelto')
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha solucionado el fraude {NoFraude}"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            self.page.update()
        except Exception as e:
            self.page.snack_bar = SnackBar(
                ft.Text(f"No se ha podido solucionar el fraude {NoFraude}"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'red'
            self.page.update()
            print(e)

    def BorrarParentezco(self, DPI1, DPI2):
        try:
            self.backend.delete_parentesco_tipo(DPI1, DPI2)
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha borrado el parentezco entre {DPI1} y {DPI2} exitosamente"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            self.page.update()
        except Exception as e:
            self.page.snack_bar = SnackBar(
                ft.Text(f"No se ha podido borrar el parentezco entre {DPI1} y {DPI2} exitosamente"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'red'
            self.page.update()
            print(e)

    # FALTA AGREGARLE FRONTEND
    def ActivarCuentas(self, NoCuenta):
        try:
            self.backend.activate_account(NoCuenta)
            self.page.snack_bar = SnackBar(
                ft.Text(f"Se ha habilitado correctamente la cuenta {NoCuenta}"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'green'
            self.page.update()
        except:
            self.page.snack_bar = SnackBar(
                ft.Text(f"No se ha habilitar la cuente {NoCuenta}"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'red'
            self.page.update()
