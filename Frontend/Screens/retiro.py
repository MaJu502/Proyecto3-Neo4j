from flet import *
import flet as ft
from .components import InputText, Button


class Retiro(UserControl):
    def __init__(self, page, height):
        super().__init__()
        self.page = page
        self.DPI = None
        self.height = height

    def build(self):
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
                                           padding=padding.only(
                                               10, 30, 10, 30),
                                           width=450,
                                           height=450,
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
                                                       on_click=lambda _:self.page.go(
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
