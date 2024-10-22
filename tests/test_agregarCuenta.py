import pytest
from unittest.mock import MagicMock, ANY
from flet import Page
from Frontend.Screens.agregarCuenta import AddCuenta

def test_crear_cuenta():
    # Crear mocks para page y backend
    page = MagicMock(spec=Page)
    backend = MagicMock()

    # Crear instancia de AddCuenta
    add_cuenta = AddCuenta(page, 800, backend)

    # Simulamos los valores de entrada
    tipo_input = "Ahorro"
    divisa_input = "Quetzales"
    banco_input = "BI"
    dpi_input = "123456789"
    cuenta_input = "12345678"

    # Set the return value of check_account_exists before calling CrearCuenta
    backend.check_account_exists.return_value = False

    # Llamamos a la función CrearCuenta
    add_cuenta.CrearCuenta(tipo_input, divisa_input, banco_input, dpi_input, cuenta_input)

    # Verificar si la cuenta existe
    backend.check_account_exists.assert_called_with(cuenta_input)

    # Llamada para crear el nodo 'Cuenta' en el backend
    backend.create_node.assert_called_with(
        ['Cuenta'],
        {
            'numero_cuenta': cuenta_input,
            'habilitada': True,
            'tipo_cuenta': tipo_input,
            'divisa': divisa_input,
            'fecha_apertura': ANY,  # Cualquier valor de fecha
            'banco': banco_input
        }
    )

def test_cuenta_existente_con_propietario():
    # Crear mocks para page y backend
    page = MagicMock(spec=Page)
    backend = MagicMock()

    # Crear instancia de AddCuenta
    add_cuenta = AddCuenta(page, 800, backend)

    # Simulamos los valores de entrada
    tipo_input = "Monetaria"
    divisa_input = "Dolares"
    banco_input = "BAC"
    dpi_input = "987654321"
    cuenta_input = "87654321"

    # Simular que la cuenta ya existe
    backend.check_account_exists.return_value = True
    backend.get_cliente_dpi.return_value = "123456789"

    # Llamar a la función CrearCuenta
    add_cuenta.CrearCuenta(tipo_input, divisa_input, banco_input, dpi_input, cuenta_input)

    # Verificar que se ha llamado a check_account_exists
    backend.check_account_exists.assert_called_with(cuenta_input)

    # Verificar si se ha llamado a la relación tiene_cuenta con el propietario existente
    backend.create_tiene_cuenta_relationship.assert_called_with(
        cuenta_input, dpi_input, "123456789", True, ANY
    )

def test_cuenta_existente_sin_propietario():
    # Crear mocks para page y backend
    page = MagicMock(spec=Page)
    backend = MagicMock()

    # Crear instancia de AddCuenta
    add_cuenta = AddCuenta(page, 800, backend)

    # Simulamos los valores de entrada
    tipo_input = "Ahorro"
    divisa_input = "Quetzales"
    banco_input = "BI"
    dpi_input = "123456789"
    cuenta_input = "12345678"

    # Simular que la cuenta ya existe pero no tiene propietario
    backend.check_account_exists.return_value = True
    backend.get_cliente_dpi.return_value = None

    # Llamar a la función CrearCuenta
    add_cuenta.CrearCuenta(tipo_input, divisa_input, banco_input, dpi_input, cuenta_input)

    # Verificar si se llama a la función para crear una relación 'tiene_cuenta' con el DPI dado
    backend.create_tiene_cuenta_relationship.assert_called_with(
        cuenta_input, dpi_input, dpi_input, True, ANY
    )
