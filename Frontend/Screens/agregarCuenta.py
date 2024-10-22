from flet import UserControl,  UserControl, Text, ElevatedButton, Container, Row, Column, TextField, Dropdown, Image, padding, margin, border_radius, alignment, TextStyle
import flet as ft
from datetime import datetime

class AddCuenta(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.backend = backend
        self.height = height

    # Helper function to create Dropdown controls
    def create_dropdown(self, hint_text, options, width=155, height=48):
        return Dropdown(
            width=width,
            height=height,
            color='grey',
            bgcolor='#1D242D',
            focused_bgcolor='#1D242D',
            hint_text=hint_text,
            hint_style=TextStyle(color='#666C75'),
            filled=False,
            content_padding=padding.only(left=15),
            border_color='#666C75',
            options=[ft.dropdown.Option(option) for option in options]
        )

    # Helper function to create TextField controls
    def create_textfield(self, label, width=320, height=48):
        return TextField(
            label=label,
            label_style=TextStyle(color='#666C75'),
            color='white',
            width=width,
            height=height,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )

    def build(self):
        tipo_input = self.create_dropdown('Tipo', ["Ahorro", "Monetaria"])
        divisa_input = self.create_dropdown('Divisa', ["Quetzales", "Dolares"])
        banco_input = self.create_dropdown('Banco', ["BAC", "BI", "GYT", "BAM", "ANTIGUA", "WESTERN", "USBANK"], width=320)

        # Using the helper function to create text fields
        dpi_input = self.create_textfield('DPI')
        cuenta_input = self.create_textfield('No. de cuenta')

        return Container(
            expand=True,
            bgcolor='#15191E',
            content=Column(
                alignment='center',
                horizontal_alignment='center',
                controls=[
                    Container(
                        margin=margin.only(bottom=50),
                        content=Text(
                            "CREAR CUENTA",
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
                                    src='https://cdni.iconscout.com/illustration/premium/thumb/face-unlock-and-pin-security-2523248-2117424.png?f=webp')
                            ),
                            Container(
                                padding=padding.only(10, 30, 10, 30),
                                width=450,
                                height=470,
                                border_radius=border_radius.all(10),
                                bgcolor='#1D242D',
                                content=Column(
                                    alignment='center',
                                    horizontal_alignment='center',
                                    controls=[
                                        Container(
                                            margin=margin.only(bottom=20),
                                            content=Text(
                                                "Información",
                                                size=30,
                                                color='#ffffff',
                                                weight='bold',
                                            ),
                                        ),
                                        Row([tipo_input, divisa_input], alignment='center'),
                                        banco_input,
                                        dpi_input,
                                        cuenta_input,
                                        Container(
                                            alignment=alignment.center,
                                            margin=margin.only(top=15),
                                            content=ElevatedButton(
                                                on_click=lambda _: self.CrearCuenta(
                                                    tipo_input.value, divisa_input.value,
                                                    banco_input.value, dpi_input.value, cuenta_input.value),
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
                                    ]
                                )
                            ),
                        ],
                        alignment='center'
                    )
                ]
            )
        )

    def CrearCuenta(self, tipo, divisa, banco, dpi, num_cuenta):
        existe_cuenta = self.backend.check_account_exists(num_cuenta)

        if existe_cuenta:
            dpi_owner = self.backend.get_cliente_dpi(num_cuenta)
            if dpi_owner is not None:
                self.backend.create_tiene_cuenta_relationship(
                    num_cuenta, dpi, dpi_owner, True, datetime.now())
            else:
                self.backend.create_tiene_cuenta_relationship(
                    num_cuenta, dpi, dpi, True, datetime.now())
        else:
            self.backend.create_node(['Cuenta'], {
                'numero_cuenta': num_cuenta,
                'habilitada': True,
                'tipo_cuenta': tipo,
                'divisa': divisa,
                'fecha_apertura': datetime.now(),
                'banco': banco
            })

            self.backend.create_owner_relationship(
                num_cuenta, dpi, datetime.now(), datetime.now(), 'Ninguno.')
