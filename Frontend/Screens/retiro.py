from flet import *
import flet as ft
from .components import InputText, Button
from datetime import datetime


class Retiro(UserControl):
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
        dpiInput = TextField(
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
                                                   content=dpiInput
                                               ),
                                               Container(
                                                   alignment=alignment.center,
                                                   content=descInput
                                               ),
                                               Container(
                                                   alignment=alignment.center,
                                                   margin=margin.only(top=15),
                                                   content=ElevatedButton(
                                                       on_click=lambda _:self.CrearRetiro(
                                                           montoInput.value, divisaInput.value, cuentaOInput.value, dpiInput.value, descInput.value),
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

    def CrearRetiro(self, monto, divisa, cuentaOrigen, dpi, descripcion):
        promedio = self.backend.find_average_retiro_amount(cuentaOrigen)
        destinoHabilitada = self.backend.is_account_enabled(cuentaOrigen)
        dpi_owner = self.backend.get_cliente_dpi(cuentaOrigen)

        if destinoHabilitada:
            numero_para_retiro = self.backend.get_max_withdrawal_number()
            if numero_para_retiro == None:
                numero_para_retiro = 1
            else:
                numero_para_retiro += 1

            self.backend.create_node(['Retiro'], {
                'monto': int(monto),
                'fecha': datetime.now(),
                'divisa': divisa,
                'descripcion': descripcion,
                'estado': True,
                'numero_retiro': numero_para_retiro
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
            if dpi == dpi_owner:
                self.backend.create_withdrawal_relationship(
                    numero_para_retiro, cuentaOrigen, dpi, monto, divisa, datetime.now(), True)
            else:
                self.backend.create_withdrawal_relationship(
                    numero_para_retiro, cuentaOrigen, dpi, monto, divisa, datetime.now(), False)

        else:
            print(' >> Cuenta no habilitada ERROR')

        if hacerFraude:
            num_para_fraude = self.backend.get_max_fraud_number()

            if num_para_fraude == None:
                num_para_fraude = 1
            else:
                num_para_fraude += 1

            self.backend.create_node(['Fraude'], {
                'tipo': 'Retiro',
                'motivo': tipo_fraude,
                'estado': False,
                'fecha_alerta': datetime.now(),
                'accion_tomada': 'Ninguna',
                'numero_fraude': num_para_fraude
            })
            self.backend.create_fraud_relationship_retiro(
                numero_para_retiro, num_para_fraude, cuentaOrigen, monto, divisa, datetime.now(), tipo_fraude)

            # deshabilitar cuenta
            self.backend.disable_account(cuentaOrigen)

        pass
