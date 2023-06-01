from flet import *
import flet as ft
from .components import InputText, Button


class Login(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.height = height
        self.backend = backend
        self.admin = False

    def build(self):
        dpiInput = InputText('DPI', False, 280)
        adminCheckbox = Checkbox()

        return Container(
            alignment=alignment.center,
            height=self.height,
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
                                    content=dpiInput
                                ),
                                Column(alignment='center',
                                       controls=[
                                           adminCheckbox,
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
                                on_click=lambda _:self.LogInAction(
                                    dpiInput.value,
                                    adminCheckbox.value),
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
                            on_click=lambda _:self.page.go('/signup'),
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

    def LogInAction(self, DPI, adminValue):
        self.admin = adminValue
        result = self.backend.find_and_return_node('Cliente', 'DPI', DPI)
        if result:
            self.page.go('/home')
        else:
            self.page.snack_bar = SnackBar(
                ft.Text(f"Usuario no encontrado"))
            self.page.snack_bar.open = True
            self.page.snack_bar.bgcolor = 'red'
            self.page.update()
