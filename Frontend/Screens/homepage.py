from random import choice
from flet import *
import flet as ft
from flet import animation, alignment, border, transform, padding

from .transferencia import Transferencia
from .retiro import Retiro


class create_homepage(UserControl):
    def __init__(self, page, Admin=False):
        super().__init__()
        self.page = page
        self.Admin = Admin

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
                switch_control.controls.append(page2)
            elif my_index == 3:
                switch_control.controls.append(page2)
            switch_control.update()
            self.page.update()

        Destinations = None
        if self.Admin == False:
            Destinations = [
                NavigationDestination(
                    icon="send_to_mobile", label='Transferencias'),
                NavigationDestination(icon="request_quote", label='Retiro'),
            ]
        else:
            Destinations = [
                NavigationDestination(
                    icon="send_to_mobile", label='Transferencias'),
                NavigationDestination(icon="request_quote", label='Retiro'),
                NavigationDestination(icon="bar_chart", label='Estadisticas'),
                NavigationDestination(
                    icon="supervisor_account", label='Cuentas'),
            ]

        barMenu = NavigationBar(
            bgcolor="blue",
            on_change=changetab,
            selected_index=0,
            destinations=Destinations
        )

        page1 = Transferencia(self.page, self.page.height)

        page2 = Retiro(self.page, self.page.height)

        page3 = Retiro(self.page, self.page.height)

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
                        content=barMenu
                    ),
                    Container(
                        expand=True,
                        content=switch_control
                    ),
                ]
            )

        )
