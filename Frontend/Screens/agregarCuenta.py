from flet import *
import flet as ft
from .components import InputText, Button
from datetime import datetime


class AddCuenta(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.backend = backend
        self.height = height

    def build(self):
        tipoInput = Dropdown(
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
                    "Ahorro"),
                ft.dropdown.Option(
                    "Monetaria"),
            ],
        )

        divisaInput = Dropdown(
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

        bancoInput = Dropdown(
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

        dpiInput = TextField(
            label='DPI',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            width=320,
            height=48,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )

        cuentaInput = TextField(
            label='No. de cuenta',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            width=320,
            height=48,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )

        return Container(
            expand=True,
            bgcolor='#15191E',
            content=Column(alignment='center',
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
                                           padding=padding.only(
                                               10, 30, 10, 30),
                                           width=450,
                                           height=470,
                                           border_radius=border_radius.all(10),
                                           bgcolor='#1D242D',
                                           content=Column([
                                               Container(
                                                   margin=margin.only(
                                                       bottom=20),
                                                   content=Text(
                                                       "Información",
                                                       size=30,
                                                       color='#ffffff',
                                                       weight='bold',
                                                   ),
                                               ),
                                               Row([
                                                   tipoInput,
                                                   divisaInput,
                                               ], alignment='center'),
                                               bancoInput,
                                               dpiInput,
                                               cuentaInput,
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.CrearCuenta(
                                                           tipoInput.value, divisaInput.value, bancoInput.value, dpiInput.value, cuentaInput.value),
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



                                   ], alignment='center'
                               )])
        )

    def CrearCuenta(self, tipo, divisa, banco, dpi, num_cuenta):
        exite_cuenta = self.backend.check_account_exists(num_cuenta)

        if exite_cuenta:
            dpi_owner = self.backend.get_cliente_dpi(num_cuenta)
            if dpi_owner != None:
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

        pass
