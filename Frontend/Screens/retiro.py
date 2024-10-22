from flet import UserControl,  alignment, margin, Container, TextField, ElevatedButton, Dropdown, TextStyle, Column, Row, padding, Image, border_radius, Text
import flet as ft
from .components import input_text
from datetime import datetime


class Retiro(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.backend = backend
        self.height = height

    def build(self):
        monto_input = input_text(
            'Monto', False, 155)

        divisa_input = Dropdown(
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
        cuenta_o_input = TextField(
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
        dpi_input = TextField(
            label='DPI',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        desc_input = TextField(
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
                                               src='https://cdni.iconscout.com/illustration/premium/thumb/add-money-to-wallet-2523246-2117422.png?f=webp')
                                       ),
                                       Container(
                                           padding=padding.only(
                                               10, 30, 10, 30),
                                           width=450,
                                           height=520,
                                           border_radius=border_radius.all(
                                               10),
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
                                                   Container(
                                                       alignment=alignment.center,
                                                       content=monto_input
                                                   ),
                                                   Container(
                                                       alignment=alignment.center,
                                                       content=divisa_input
                                                   ),
                                               ], alignment='center'),
                                               Container(
                                                   alignment=alignment.center,
                                                   content=cuenta_o_input
                                               ),
                                               Container(
                                                   alignment=alignment.center,
                                                   content=dpi_input
                                               ),
                                               Container(
                                                   alignment=alignment.center,
                                                   content=desc_input
                                               ),
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.CrearRetiro(
                                                           monto_input.value, divisa_input.value, cuenta_o_input.value, dpi_input.value, desc_input.value),
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

    def CrearRetiro(self, monto, divisa, cuenta_origen, dpi, descripcion):
        promedio = self.backend.find_average_retiro_amount(cuenta_origen)
        destino_habilitada = self.backend.is_account_enabled(cuenta_origen)
        dpi_owner = self.backend.get_cliente_dpi(cuenta_origen)

        if not destino_habilitada:
            print(' >> Cuenta no habilitada ERROR')
            return

        numero_para_retiro = self.obtener_numero_para_retiro()

        self.crear_retiro(cuenta_origen, monto, divisa, descripcion, numero_para_retiro)

        hacer_fraude, tipo_fraude = self.verificar_fraude(cuenta_origen, monto, promedio)

        self.realizar_retiro(dpi, dpi_owner, numero_para_retiro, cuenta_origen, monto, divisa)

        if hacer_fraude:
            self.reportar_fraude(cuenta_origen, numero_para_retiro, monto, divisa, tipo_fraude)


    def obtener_numero_para_retiro(self):
        numero_para_retiro = self.backend.get_max_withdrawal_number()
        return 1 if numero_para_retiro is None else numero_para_retiro + 1


    def crear_retiro(self, cuenta_origen, monto, divisa, descripcion, numero_para_retiro):
        self.backend.create_node(['Retiro'], {
            'monto': int(monto),
            'fecha': datetime.now(),
            'divisa': divisa,
            'descripcion': descripcion,
            'estado': True,
            'numero_retiro': numero_para_retiro
        })


    def verificar_fraude(self, cuenta_origen, monto, promedio):
        hacer_fraude = False
        tipo_fraude = 'Ninguno'
        if int(monto) > 100000:
            hacer_fraude = True
            tipo_fraude = 'Monto elevado'
        if int(monto) > promedio:
            hacer_fraude = True
            tipo_fraude = 'Monto fuera de promedio'
        if self.backend.has_relationship_with_fraud(cuenta_origen):
            hacer_fraude = True
            tipo_fraude = 'Cuenta anormal ligada a fraude'
        return hacer_fraude, tipo_fraude


    def realizar_retiro(self, dpi, dpi_owner, numero_para_retiro, cuenta_origen, monto, divisa):
        if dpi == dpi_owner:
            self.backend.create_withdrawal_relationship(
                numero_para_retiro, cuenta_origen, dpi, monto, divisa, datetime.now(), True)
        else:
            self.backend.create_withdrawal_relationship(
                numero_para_retiro, cuenta_origen, dpi, monto, divisa, datetime.now(), False)


    def reportar_fraude(self, cuenta_origen, numero_para_retiro, monto, divisa, tipo_fraude):
        num_para_fraude = self.backend.get_max_fraud_number()
        num_para_fraude = 1 if num_para_fraude is None else num_para_fraude + 1

        self.backend.create_node(['Fraude'], {
            'tipo': 'Retiro',
            'motivo': tipo_fraude,
            'estado': False,
            'fecha_alerta': datetime.now(),
            'accion_tomada': 'Ninguna',
            'numero_fraude': num_para_fraude
        })
        self.backend.create_fraud_relationship_retiro(
            numero_para_retiro, num_para_fraude, cuenta_origen, monto, divisa, datetime.now(), tipo_fraude)
        self.backend.disable_account(cuenta_origen)
