from flet import UserControl,  Text, Container, ElevatedButton, Column, alignment, TextField, Dropdown, margin, padding, border_radius, Image, Row, TextStyle
import flet as ft
from .components import input_text
from datetime import datetime

# Constantes
NO_CUENTA_LABEL = 'No. Cuenta'


class Transferencia(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.backend = backend
        self.height = height

    # Helper function to create TextField components
    def create_textfield(self, label, width=320, height=48, multiline=False, min_lines=1, max_lines=1):
        return TextField(
            label=label,
            label_style=TextStyle(color='#666C75'),
            color='white',
            height=height,
            width=width,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
            multiline=multiline,
            min_lines=min_lines,
            max_lines=max_lines
        )

    # Helper function to create Container with a title
    def create_title_container(self, title, size=30, color='#ffffff', weight='bold', margin_bottom=20):
        return Container(
            margin=margin.only(bottom=margin_bottom),
            content=Text(
                title,
                size=size,
                color=color,
                weight=weight,
            ),
        )

    def build(self):
        monto_input = input_text('Monto', False, 155)

        divisa_input = Dropdown(
            width=155,
            height=48,
            color='grey',
            bgcolor='#1D242D',
            focused_bgcolor='#1D242D',
            hint_text='Divisa',
            hint_style=TextStyle(color='#666C75'),
            filled=False,
            content_padding=padding.only(left=15),
            border_color='#666C75',
            options=[
                ft.dropdown.Option("Quetzales"),
                ft.dropdown.Option("Dolares"),
            ],
        )

        # Using the helper function to create text fields
        cuenta_o_input = self.create_textfield(NO_CUENTA_LABEL + ' Origen')
        cuenta_d_input = self.create_textfield(NO_CUENTA_LABEL + ' Destino')
        desc_input = self.create_textfield('Descripcion', multiline=True, min_lines=3, max_lines=3)

        return Container(
            expand=True,
            bgcolor='#15191E',
            content=Column(
                alignment='center',
                horizontal_alignment='center',
                controls=[
                    self.create_title_container("TRANSFERENCIAS", size=100, color='blue'),
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
                                height=520,
                                border_radius=border_radius.all(10),
                                bgcolor='#1D242D',
                                content=Column(
                                    alignment='center',
                                    horizontal_alignment='center',
                                    controls=[
                                        self.create_title_container("Información", size=30),
                                        Row(
                                            alignment='center',
                                            controls=[
                                                Container(
                                                    alignment=alignment.center,
                                                    content=monto_input
                                                ),
                                                Container(
                                                    alignment=alignment.center,
                                                    content=divisa_input
                                                ),
                                            ]
                                        ),
                                        Container(alignment=alignment.center, content=cuenta_o_input),
                                        Container(alignment=alignment.center, content=cuenta_d_input),
                                        Container(alignment=alignment.center, content=desc_input),
                                        Container(
                                            alignment=alignment.center,
                                            margin=margin.only(top=15),
                                            content=ElevatedButton(
                                                on_click=lambda _: self.CrearTransferencia(
                                                    monto_input.value, divisa_input.value,
                                                    cuenta_o_input.value, cuenta_d_input.value,
                                                    desc_input.value),
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
                                    ]
                                )
                            ),
                        ],
                        alignment='center'
                    )
                ]
            )
        )

    def verificar_condiciones_fraude(self, monto, promedio, cuenta_origen):
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

    def CrearTransferencia(self, monto, divisa, cuenta_origen, cuenta_destino, descripcion):
        promedio = self.backend.find_average_transfer_amount(cuenta_origen)
        destino_habilitada = self.backend.is_account_enabled(cuenta_destino)

        if not destino_habilitada:
            print(' >> Cuenta no habilitada ERROR')
            return

        numero_para_transfer = self.backend.get_max_transaction_number() or 1
        ach_o_no = self.backend.compare_account_banks(cuenta_origen, cuenta_destino)

        tipo_transfer = '3ero' if ach_o_no else 'ach'
        self.backend.create_node(['Transferencia'], {
            'monto': int(monto),
            'fecha': datetime.now(),
            'divisa': divisa,
            'tipo_transfer': tipo_transfer,
            'descripcion': descripcion,
            'numero_transferencia': numero_para_transfer
        })

        # Verificar condiciones de fraude
        hacer_fraude, tipo_fraude = self.verificar_condiciones_fraude(monto, promedio * 1.5 if promedio else 0, cuenta_origen)

        # Hacer la transferencia
        self.backend.create_transaccion_relationship(
            cuenta_origen, cuenta_destino, numero_para_transfer, divisa, int(monto), datetime.now(),
            self.backend.get_account_type(cuenta_destino))

        if hacer_fraude:
            self.crear_nodo_fraude(numero_para_transfer, cuenta_origen, cuenta_destino, tipo_fraude, monto)

    def crear_nodo_fraude(self, numero_para_transfer, cuenta_origen, cuenta_destino, tipo_fraude, monto):
        num_para_fraude = self.backend.get_max_fraud_number() or 1
        self.backend.create_node(['Fraude'], {
            'tipo': 'Transferencia',
            'motivo': tipo_fraude,
            'estado': False,
            'fecha_alerta': datetime.now(),
            'accion_tomada': 'Ninguna',
            'numero_fraude': num_para_fraude
        })

        self.backend.create_fraud_relationship_transferencia(
            numero_para_transfer, num_para_fraude, cuenta_origen, tipo_fraude, monto, datetime.now())

        self.backend.create_fraud_relationship_transferencia(
            numero_para_transfer, num_para_fraude, cuenta_destino, tipo_fraude, monto, datetime.now())

        self.backend.disable_account(cuenta_origen)
