from unittest import TestCase
from unittest.mock import MagicMock, patch, call, ANY
from datetime import datetime
from Frontend.Screens.transferencia import Transferencia

class TestTransferencia(TestCase):
    def setUp(self):
        # Configura un mock para el backend y crea una instancia de Transferencia
        self.mock_backend = MagicMock()
        self.transferencia = Transferencia(MagicMock(), 500, self.mock_backend)

    @patch('Frontend.Screens.transferencia.input_text')
    @patch('Frontend.Screens.transferencia.Dropdown')
    def test_build(self, mock_dropdown, mock_input_text):
        # Mock the input_text and Dropdown components
        mock_input_text.side_effect = lambda label, hide, width: MagicMock()
        mock_dropdown.return_value = MagicMock()

        # Call the build method
        container = self.transferencia.build()

        # Verify that container has some expected structure
        self.assertIsNotNone(container.content)  # Confirm content exists

    @patch('Frontend.Screens.transferencia.datetime')
    def test_crear_nodo_fraude(self, mock_datetime):
        # Simular la fecha actual
        mock_datetime.now.return_value = datetime(2024, 10, 18, 17, 1, 8)

        # Mockear el valor de numero_fraude
        self.mock_backend.get_max_fraud_number.return_value = 1

        # Mock the values
        numero_para_transfer = 1
        cuenta_origen = '12345'
        cuenta_destino = '67890'
        tipo_fraude = 'Monto elevado'
        monto = 150000

        # Call the crear_nodo_fraude method
        self.transferencia.crear_nodo_fraude(numero_para_transfer, cuenta_origen, cuenta_destino, tipo_fraude, monto)

        # Verify that create_node for 'Fraude' was called
        self.mock_backend.create_node.assert_called_once_with(
            ['Fraude'],
            {
                'tipo': 'Transferencia',
                'motivo': tipo_fraude,
                'estado': False,
                'fecha_alerta': datetime(2024, 10, 18, 17, 1, 8),
                'accion_tomada': 'Ninguna',
                'numero_fraude': 1
            }
        )

    @patch('Frontend.Screens.transferencia.datetime')
    def test_crear_transferencia(self, mock_datetime):
        # Set a static time for the test
        mock_datetime.now.return_value = datetime(2024, 10, 18, 17, 1, 8)

        # Set up inputs for CrearTransferencia
        monto = 10000
        divisa = "Quetzales"
        cuenta_origen = "12345"
        cuenta_destino = "67890"
        descripcion = "Payment for services"

        # Mock backend methods
        self.mock_backend.find_average_transfer_amount.return_value = 8000
        self.mock_backend.is_account_enabled.return_value = True
        self.mock_backend.get_max_transaction_number.return_value = 5
        self.mock_backend.compare_account_banks.return_value = False

        # Call the CrearTransferencia method
        self.transferencia.CrearTransferencia(monto, divisa, cuenta_origen, cuenta_destino, descripcion)

        # Verify that create_node was called with expected arguments
        self.mock_backend.create_node.assert_has_calls([
            call(['Transferencia'], {
                'monto': monto,
                'fecha': datetime(2024, 10, 18, 17, 1, 8),
                'divisa': divisa,
                'tipo_transfer': 'ach',
                'descripcion': descripcion,
                'numero_transferencia': 5
            }),
            call(['Fraude'], ANY)  # Verifica que se crea el nodo de fraude
        ])

    def verificar_condiciones_fraude(self, monto, promedio, cuenta_origen):
        hacer_fraude = False
        tipo_fraude = 'Ninguno'

        # Priorizar la condición de monto elevado
        if int(monto) > 100000:
            hacer_fraude = True
            tipo_fraude = 'Monto elevado'
        elif int(monto) > promedio:
            hacer_fraude = True
            tipo_fraude = 'Monto fuera de promedio'
        elif self.backend.has_relationship_with_fraud(cuenta_origen):
            hacer_fraude = True
            tipo_fraude = 'Cuenta anormal ligada a fraude'

        return hacer_fraude, tipo_fraude
