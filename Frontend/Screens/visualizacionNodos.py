from flet import UserControl,  Container, Column, ElevatedButton, TextStyle, Dropdown, padding, Row, margin, Text, alignment, ScrollMode
import flet as ft
from datetime import datetime

class VisualizacionNodos(UserControl):
    def __init__(self, page, height, backend):
        super().__init__()
        self.page = page
        self.DPI = None
        self.backend = backend
        self.height = height

    def build(self):

        opciones = Dropdown(
            height=48,
            color='grey',
            bgcolor='#1D242D',
            focused_bgcolor='#1D242D',
            hint_text='Seleccione una opción',
            hint_style=TextStyle(
                color='#666C75'),
            filled=False,
            content_padding=padding.only(
                left=15),
            border_color='#666C75',
            options=[
                ft.dropdown.Option(
                    key=1, text="Top 5 cuentas con fraudes"),
                ft.dropdown.Option(
                    key=2, text="Usuarios implicados en fraudes"),
                ft.dropdown.Option(
                    key=3, text="Fraudes en cada banco"),
                ft.dropdown.Option(
                    key=4, text="Top 5 transferencias más altas"),
                ft.dropdown.Option(
                    key=5, text="Top 5 retiros más altos"),
            ],
        )

        self.mainView = Column(alignment='start',
                            horizontal_alignment='center',
                            controls=[
                                Row(
                                    vertical_alignment='center',
                                    alignment='spaceBetween',
                                    controls=[
                                        Container(
                                            margin=margin.only(
                                                left=30, bottom=10, top=10, right=0),
                                            content=Text(
                                                "VISUALIZACIÓN",
                                                size=60,
                                                color='white',
                                                weight='bold',
                                            ),
                                        ),
                                        Row(
                                            spacing=0,
                                            controls=[
                                                Container(

                                                    margin=margin.only(
                                                        left=0, bottom=10, top=10, right=20),
                                                    content=opciones
                                                ),
                                                Container(
                                                    alignment=alignment.center,
                                                    margin=margin.only(
                                                        left=0, bottom=10, top=10, right=30),
                                                    content=ElevatedButton(
                                                        on_click=lambda _:self.VisualizarEstadisticas(
                                                            opciones.value),
                                                        content=Text(
                                                            'Consultar',
                                                            size=15,
                                                            weight='bold',
                                                            color="white"
                                                        ),
                                                        height=48,
                                                        width=180,
                                                        bgcolor='#0162A8'
                                                    )
                                                ),
                                            ], alignment='center', vertical_alignment='center'
                                        ),
                                    ]
                                ),
                            ])

        return Container(
            expand=True,
            height=self.height,
            bgcolor='#15191E',
            content=self.mainView
        )

    def generateTop(self, lista, color):
        count = 1
        nodes = []
        for result in lista:
            nodes.append(self.generateNode(result[0], result[1], count, color))
            count += 1
        lista1 = nodes[:2]
        lista2 = nodes[2:]

        return Column(
            alignment='spaceAround',
            horizontal_alignment='center',
            controls=[
                Row(
                    alignment='center',
                    controls=lista1
                ),
                Row(
                    alignment='center',
                    controls=lista2
                ),
            ]
        )

    def generateCount(self, lista, value, color):
        count = 1
        nodes = []
        for result in lista:
            nodes.append(self.generateCliente(
                result[0], result[1], count, value, color))
            count += 1

        return Column(
            alignment='spaceAround',
            horizontal_alignment='center',
            controls=[
                Row(
                    scroll=ScrollMode.AUTO,
                    alignment='center',
                    controls=nodes
                ),
            ]
        )

    def generateNode(self, title, nume, count, color):

        return Container(
            width=180,
            height=180,
            bgcolor=color,
            border_radius=180,
            margin=20,
            content=Column([
                Text(count, size=26, color='white', weight='bold'),
                Text(f'Cuenta No.{title}', size=20, weight='bold'),
                Text(nume, size=16),
            ], alignment='center', horizontal_alignment='center')
        )

    def generateCliente(self, title, nume, count, value, color):

        return Container(
            width=180,
            height=180,
            bgcolor=color,
            border_radius=180,
            margin=20,
            content=Column([
                Text(count, size=26, color='white', weight='bold'),
                Text(title, size=20, weight='bold'),
                Text(f'{value}: {nume}', size=15),
            ], alignment='center', horizontal_alignment='center')
        )

    def VisualizarEstadisticas(self, opcion):
        self.limpiar_vista()

        if opcion == '1':
            self.mostrar_estadisticas(
                titulo="TOP 5 CUENTAS CON MAS FRAUDES",
                datos=self.backend.get_top_accounts_with_fraud_relations(),
                color='#FFD0CA',
                tipo='top'
            )
        elif opcion == '2':
            self.mostrar_estadisticas(
                titulo="CLIENTES IMPLICADOS EN FRAUDES",
                datos=self.backend.get_client_names_related_to_fraud(),
                color='#AECCB3',
                tipo='count',
                value='DPI'
            )
        elif opcion == '3':
            dicc = self.backend.count_banks_related_to_fraud()
            lista = [(key, value) for key, value in dicc.items()]
            self.mostrar_estadisticas(
                titulo="FRAUDES REGISTRADOS POR BANCO",
                datos=lista,
                color='#A6A0B2',
                tipo='count',
                value='Fraudes'
            )
        elif opcion == '4':
            self.mostrar_estadisticas(
                titulo="TOP 5 TRANSFERENCIAS CON MONTOS MAS ALTOS",
                datos=self.backend.get_top_5_high_amount_transactions_related_to_fraud(),
                color='#ADCDFF',
                tipo='top'
            )
        elif opcion == '5':
            self.mostrar_estadisticas(
                titulo="TOP 5 RETIROS CON MONTOS MAS ALTOS",
                datos=self.backend.get_top_5_high_amount_withdrawals_related_to_fraud(),
                color='#F8D092',
                tipo='top'
            )
        else:
            return

        self.page.update()

    def limpiar_vista(self):
        """Elimina los controles existentes en la vista antes de agregar nuevos."""
        if len(self.mainView.controls) == 3:
            self.mainView.controls.pop()
            self.mainView.controls.pop()

    def mostrar_estadisticas(self, titulo, datos, color, tipo, value=None):
        """Función auxiliar para mostrar las estadísticas según la opción."""
        self.mainView.controls.append(Container(content=Text(titulo, size=60, color='white')))

        if tipo == 'top':
            self.mainView.controls.append(self.generateTop(datos, color))
        elif tipo == 'count' and value:
            self.mainView.controls.append(self.generateCount(datos, value, color))

        self.mainView.update()