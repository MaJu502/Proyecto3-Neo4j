import unittest
from unittest.mock import patch, MagicMock
from Frontend.Screens.signup import SignUp
from flet import Page
import datetime

class TestSignUp(unittest.TestCase):

    def setUp(self):
        # Mock the Page and Backend objects
        self.mock_page = MagicMock(spec=Page)
        self.mock_backend = MagicMock()

        # Create an instance of SignUp
        self.signup = SignUp(self.mock_page, 500, self.mock_backend)

    @patch('Frontend.Screens.signup.input_text')
    @patch('Frontend.Screens.signup.Checkbox')
    def test_build(self, mock_checkbox, mock_input_text):
        # Mock input_text and checkbox components
        mock_input_text.side_effect = lambda label, hide, width: MagicMock()
        mock_checkbox.return_value = MagicMock()

        # Call the build function
        container = self.signup.build()

        # Check if the container has the expected structure
        self.assertEqual(container.height, 500)
        self.assertTrue(container.content)

        # Check that input_text was called for each form field
        mock_input_text.assert_any_call('Nombre', False, 155)
        mock_input_text.assert_any_call('Apellido', False, 155)
        mock_input_text.assert_any_call('DPI', False, 270)
        mock_input_text.assert_any_call('Direccion', False, 320)
        mock_input_text.assert_any_call('Fecha de nacimiento', False, 320)

        # Verify that the checkbox was called for admin
        mock_checkbox.assert_called_once()

    def test_crear_nodo(self):
        # Set up inputs for CrearNodo
        nombre = "John"
        apellido = "Doe"
        dpi = "123456789"
        direccion = "123 Main St"
        date = "1990-01-01"
        admin = True

        # Call the CrearNodo method
        self.signup.CrearNodo(nombre, apellido, dpi, direccion, date, admin)

        # Check if the create_node method was called with expected arguments
        self.mock_backend.create_node.assert_called_once_with(
            ['Cliente', 'Admin'],
            {
                'nombre': nombre,
                'apellido': apellido,
                'direccion': direccion,
                'DPI': dpi,
                'fecha_nacimiento': datetime.date(1990, 1, 1)
            }
        )

        # Verify that page.go was called to redirect to '/home'
        self.mock_page.go.assert_called_once_with('/home')

if __name__ == "__main__":
    unittest.main()
