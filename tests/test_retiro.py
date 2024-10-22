import unittest
from unittest.mock import MagicMock, patch
from Frontend.Screens.retiro import Retiro
from datetime import datetime

# Constantes
MONTOELEVADO_MSG = 'Monto elevado'

class TestRetiro(unittest.TestCase):

    def setUp(self):
        # Create a mock backend and mock page
        self.mock_backend = MagicMock()
        self.mock_page = MagicMock()
        self.height = 600

        # Create an instance of Retiro
        self.retiro = Retiro(self.mock_page, self.height, self.mock_backend)

    @patch('Frontend.Screens.retiro.input_text')
    @patch('Frontend.Screens.retiro.Dropdown')
    def test_build(self, mock_dropdown, mock_input_text):
        # Call the build method
        result = self.retiro.build()

        # Check if the result contains the expected properties
        self.assertIsNotNone(result)
        self.assertEqual(result.bgcolor, '#15191E')

    def test_obtener_numero_para_retiro(self):
        # Test when no previous withdrawal exists
        self.mock_backend.get_max_withdrawal_number.return_value = None
        numero_retiro = self.retiro.obtener_numero_para_retiro()
        self.assertEqual(numero_retiro, 1)

        # Test when a previous withdrawal exists
        self.mock_backend.get_max_withdrawal_number.return_value = 5
        numero_retiro = self.retiro.obtener_numero_para_retiro()
        self.assertEqual(numero_retiro, 6)

    def verificar_fraude(self, cuenta_origen, monto, promedio):
        hacer_fraude = False
        tipo_fraude = 'Ninguno'
        if int(monto) > 100000:
            hacer_fraude = True
            tipo_fraude = MONTOELEVADO_MSG  # Prioritize this message for high amounts
        elif int(monto) > promedio:
            hacer_fraude = True
            tipo_fraude = 'Monto fuera de promedio'
        if self.backend.has_relationship_with_fraud(cuenta_origen):
            hacer_fraude = True
            tipo_fraude = 'Cuenta anormal ligada a fraude'
        return hacer_fraude, tipo_fraude

    @patch('Frontend.Screens.retiro.datetime')
    def test_realizar_retiro(self, mock_datetime):
        # Set a fixed return value for datetime.now()
        mock_datetime.now.return_value = datetime(2024, 10, 18, 16, 50, 28)

        # Test when DPI matches DPI owner
        self.retiro.realizar_retiro('123', '123', 1, 'account', 1000, 'Quetzales')
        self.mock_backend.create_withdrawal_relationship.assert_called_once_with(
            1, 'account', '123', 1000, 'Quetzales', mock_datetime.now(), True
        )

    @patch('Frontend.Screens.retiro.datetime')  # Patch datetime in the retiro module
    def test_crear_retiro(self, mock_datetime):
        # Set a fixed return value for datetime.now()
        mock_datetime.now.return_value = datetime(2024, 10, 18, 16, 50, 28)

        # Test the creation of a withdrawal node
        self.retiro.crear_retiro('account', 1000, 'Quetzales', 'Test description', 1)
        self.mock_backend.create_node.assert_called_once_with(
            ['Retiro'], {
                'monto': 1000,
                'fecha': mock_datetime.now(),
                'divisa': 'Quetzales',
                'descripcion': 'Test description',
                'estado': True,
                'numero_retiro': 1
            }
        )

    @patch('Frontend.Screens.retiro.datetime')
    def test_reportar_fraude(self, mock_datetime):
        # Mock the datetime to control time
        mock_datetime.now.return_value = datetime(2024, 1, 1)

        # Test fraud reporting
        self.mock_backend.get_max_fraud_number.return_value = None
        self.retiro.reportar_fraude('account', 1, 1000, 'Quetzales', MONTOELEVADO_MSG)

        # Assert that the fraud node was created
        self.mock_backend.create_node.assert_called_once_with(
            ['Fraude'], {
                'tipo': 'Retiro',
                'motivo': MONTOELEVADO_MSG,
                'estado': False,
                'fecha_alerta': datetime(2024, 1, 1),
                'accion_tomada': 'Ninguna',
                'numero_fraude': 1
            }
        )
        # Assert that the account was disabled
        self.mock_backend.disable_account.assert_called_once_with('account')

if __name__ == '__main__':
    unittest.main()
