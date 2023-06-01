from flet import *
import flet as ft
from .components import InputText, Button
from datetime import datetime


class Transferencia(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.backend = backend
        self.height = height

    def build(self):
        montoInput = InputText(
            'Monto', False, 155)

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
        cuentaOInput = TextField(
            label='No. Cuenta Origen',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        cuentaDInput = TextField(
            label='No. Cuenta Destino',
            label_style=TextStyle(
                color='#666C75'),
            color='white',
            height=48,
            width=320,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
        )
        descInput = TextField(
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
                                                       content=montoInput
                                                   ),
                                                   Container(
                                                       alignment=alignment.center,
                                                       content=divisaInput
                                                   ),
                                               ], alignment='center'),
                                               Container(
                                                   alignment=alignment.center,
                                                   content=cuentaOInput
                                               ),
                                               Container(
                                                   alignment=alignment.center,
                                                   content=cuentaDInput
                                               ),
                                               Container(
                                                   alignment=alignment.center,
                                                   content=descInput
                                               ),
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.CrearTransferencia(
                                                           montoInput.value, divisaInput.value, cuentaOInput.value, cuentaDInput.value, descInput.value),
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

    def CrearTransferencia(self, monto, divisa, cuentaOrigen, cuentaDestino, descripcion):
        promedio = self.backend.find_average_transfer_amount(cuentaOrigen)
        destinoHabilitada = self.backend.is_account_enabled(cuentaDestino)

        if destinoHabilitada:
            numero_para_transfer = self.backend.get_max_transaction_number()
            if numero_para_transfer == None:
                numero_para_transfer = 1
            else:
                numero_para_transfer += 1
            ach_o_no = self.backend.compare_account_banks(
                cuentaOrigen, cuentaDestino)

            if ach_o_no:
                self.backend.create_node(['Transferencia'], {
                    'monto': int(monto),
                    'fecha': datetime.now(),
                    'divisa': divisa,
                    'tipo_transfer': '3ero',
                    'descripcion': descripcion,
                    'numero_transferencia': numero_para_transfer
                })
            else:
                self.backend.create_node(['Transferencia'], {
                    'monto': int(monto),
                    'fecha': datetime.now(),
                    'divisa': divisa,
                    'tipo_transfer': 'ach',
                    'descripcion': descripcion,
                    'numero_transferencia': numero_para_transfer
                })

            aplica_promedio = False
            if promedio != None:
                aplica_promedio = True
                promedio = promedio * 1.5
            else:
                promedio = 0

            # verificar condiciones de fraude
            hacerFraude = False
            tipo_fraude = 'Ninguno'
            if int(monto) > 100000:
                hacerFraude = True
                tipo_fraude = 'Monto elevado'
            if int(monto) > promedio and aplica_promedio:
                hacerFraude = True
                tipo_fraude = 'Monto fuera de promedio'
            if self.backend.has_relationship_with_fraud(cuentaOrigen):
                hacerFraude = True
                tipo_fraude = 'Cuenta anormal ligada a fraude'

            # hacer la transferencia
            self.backend.create_transaccion_relationship(
                cuentaOrigen, cuentaDestino, numero_para_transfer, divisa, int(monto), datetime.now(), self.backend.get_account_type(cuentaDestino))

        else:
            print(' >> Cuenta no habilitada ERROR')

        if hacerFraude:
            num_para_fraude = self.backend.get_max_fraud_number()

            if num_para_fraude == None:
                num_para_fraude = 1
            else:
                num_para_fraude += 1

            self.backend.create_node(['Fraude'], {
                'tipo': 'Transferencia',
                'motivo': tipo_fraude,
                'estado': False,
                'fecha_alerta': datetime.now(),
                'accion_tomada': 'Ninguna',
                'numero_fraude': num_para_fraude
            })
            self.backend.create_fraud_relationship_transferencia(
                numero_para_transfer, num_para_fraude, cuentaOrigen, tipo_fraude, monto, datetime.now())

            self.backend.create_fraud_relationship_transferencia(
                numero_para_transfer, num_para_fraude, cuentaDestino, tipo_fraude, monto, datetime.now())

            # deshabilitar cuenta
            self.backend.disable_account(cuentaOrigen)

        pass
