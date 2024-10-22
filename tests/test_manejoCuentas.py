import unittest
from unittest.mock import MagicMock, patch
from Frontend.Screens.manejoCuentas import ManejoCuentas

class TestManejoCuentas(unittest.TestCase):

    def setUp(self):
        # Create a mock for the backend and page objects
        self.mock_backend = MagicMock()
        self.mock_page = MagicMock()
        self.height = 600  # You can adjust this according to your needs

        # Instantiate the ManejoCuentas class with mocked objects
        self.manejo_cuentas = ManejoCuentas(self.mock_page, self.height, self.mock_backend)

    @patch('Frontend.Screens.manejoCuentas.TextField')
    def test_build(self, mock_textfield):
        # Call the build method
        result = self.manejo_cuentas.build()

        # Assert the layout is correctly returned
        self.assertIsNotNone(result)
        self.assertEqual(result.height, self.height)
        self.assertEqual(result.bgcolor, '#15191E')

    @patch('Frontend.Screens.manejoCuentas.SnackBar')
    def test_crear_parentesco_success(self, mock_snackbar):
        # Simulate a successful parentage creation
        self.manejo_cuentas.CrearParentezco("123", "456", "Familia", "1")
        self.mock_backend.create_parentesco_relationship.assert_called_once_with("123", "456", "Familia", "1", True)

        # Assert snack bar message was shown for success
        self.assertEqual(self.mock_page.snack_bar.bgcolor, 'green')

    @patch('Frontend.Screens.manejoCuentas.SnackBar')
    def test_crear_parentesco_failure(self, mock_snackbar):
        # Simulate an error during parentage creation
        self.mock_backend.create_parentesco_relationship.side_effect = Exception("Test error")
        self.manejo_cuentas.CrearParentezco("123", "456", "Familia", "1")

        # Assert snack bar message was shown for failure
        self.assertEqual(self.mock_page.snack_bar.bgcolor, 'red')

    @patch('Frontend.Screens.manejoCuentas.SnackBar')
    def test_borrar_cuenta_success(self, mock_snackbar):
        # Simulate a successful account deletion
        self.manejo_cuentas.BorrarCuenta("12345")
        self.mock_backend.delete_account.assert_called_once_with("12345")

        # Assert snack bar message was shown for success
        self.assertEqual(self.mock_page.snack_bar.bgcolor, 'green')

    @patch('Frontend.Screens.manejoCuentas.SnackBar')
    def test_borrar_cuenta_failure(self, mock_snackbar):
        # Simulate an error during account deletion
        self.mock_backend.delete_account.side_effect = Exception("Test error")
        self.manejo_cuentas.BorrarCuenta("12345")

        # Assert snack bar message was shown for failure
        self.assertEqual(self.mock_page.snack_bar.bgcolor, 'red')

    @patch('Frontend.Screens.manejoCuentas.SnackBar')
    def test_actualizar_motivo_success(self, mock_snackbar):
        # Simulate a successful motive update
        self.manejo_cuentas.ActualizarMotivo("12345", "1", "Nuevo Motivo")
        self.mock_backend.update_involucra_motivo.assert_called_once_with("12345", 1, "Nuevo Motivo")

        # Assert snack bar message was shown for success
        self.assertEqual(self.mock_page.snack_bar.bgcolor, 'green')

    @patch('Frontend.Screens.manejoCuentas.SnackBar')
    def test_actualizar_banco_success(self, mock_snackbar):
        # Simulate a successful bank update
        self.manejo_cuentas.ActualizarBanco("12345", "BI")
        self.mock_backend.update_cuenta_banco.assert_called_once_with("12345", "BI")

        # Assert snack bar message was shown for success
        self.assertEqual(self.mock_page.snack_bar.bgcolor, 'green')

if __name__ == '__main__':
    unittest.main()
