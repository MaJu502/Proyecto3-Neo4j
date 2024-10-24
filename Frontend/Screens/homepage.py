from random import choice
from flet import UserControl,  Container, Column, Text, ElevatedButton, margin
from flet.navigation import NavigationDestination, NavigationBar
from flet.controls import UserControl

from .transferencia import Transferencia
from .retiro import Retiro
from .manejoCuentas import ManejoCuentas
from .agregarCuenta import AddCuenta
from .visualizacionNodos import VisualizacionNodos



class create_homepage(UserControl):
    def __init__(self, page, backend, admin=False):
        super().__init__()
        self.page = page
        self.admin = admin
        self.backend = backend

    def build(self):

        def changetab(e):
            # GET INDEX TAB
            my_index = e.control.selected_index
            switch_control.controls.pop()
            if my_index == 0:
                switch_control.controls.append(page1)
            elif my_index == 1:
                switch_control.controls.append(page2)
            elif my_index == 2:
                switch_control.controls.append(page5)
            elif my_index == 3:
                switch_control.controls.append(page3)
            elif my_index == 4:
                switch_control.controls.append(page4)
            switch_control.update()
            self.page.update()

        destinations = None
        if self.admin == False:
            destinations = [
                NavigationDestination(
                    icon="send_to_mobile", label='Transferencias'),
                NavigationDestination(icon="request_quote", label='Retiro'),
                NavigationDestination(icon="add", label='Crear cuenta'),
            ]
        else:
            destinations = [
                NavigationDestination(
                    icon="send_to_mobile", label='Transferencias'),
                NavigationDestination(icon="request_quote", label='Retiro'),
                NavigationDestination(icon="add", label='Crear cuenta'),
                NavigationDestination(icon="bar_chart", label='Estadisticas'),
                NavigationDestination(
                    icon="supervisor_account", label='Cuentas'),
            ]

        bar_menu = NavigationBar(
            bgcolor="blue",
            on_change=changetab,
            selected_index=0,
            destinations=destinations
        )

        page1 = Transferencia(self.page, self.page.height, self.backend)

        page2 = Retiro(self.page, self.page.height, self.backend)

        page3 = VisualizacionNodos(self.page, self.page.height, self.backend)

        page4 = ManejoCuentas(self.page, self.page.height, self.backend)

        page5 = AddCuenta(self.page, self.page.height, self.backend)

        switch_control = Column(
            expand=False,
            controls=[
                page1,
            ]
        )

        return Container(
            expand=False,
            height=self.page.height,
            bgcolor='#1D242D',
            content=Column(
                spacing=0,
                controls=[
                    Container(
                        content=bar_menu
                    ),

                    Container(
                        expand=True,
                        content=switch_control
                    ),

                    Container(
                        width=100,
                        margin=margin.only(bottom=30, left=20),
                        content=ElevatedButton(
                            on_click=lambda _:self.page.go(
                                '/'),
                            content=Text(
                                'Salir',
                                size=15,
                                weight='bold',
                                color="white"
                            ),
                            height=48,
                            width=180,
                            bgcolor='red'
                        )
                    ),
                ]
            )

        )
