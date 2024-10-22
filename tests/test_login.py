import unittest
from unittest.mock import MagicMock, patch
from flet import Page
from Frontend.Screens.login import Login


class TestLogin(unittest.TestCase):

    def setUp(self):
        # Mock del objeto Page y backend
        self.mock_page = MagicMock(spec=Page)
        self.mock_backend = MagicMock()
        self.login_instance = Login(self.mock_page, height=600, backend=self.mock_backend)

    @patch("Frontend.Screens.login.input_text")
    @patch("Frontend.Screens.login.Checkbox")
    def test_build(self, mock_checkbox, mock_input_text):
        # Mock de los componentes de entrada
        mock_input_text.return_value = MagicMock(value="mock_dpi")
        mock_checkbox.return_value = MagicMock(value=True)

        # Llamada a la función build
        login_container = self.login_instance.build()

        # Verificamos que el input_text y el Checkbox sean llamados
        mock_input_text.assert_called_once_with('dpi', False, 280)
        mock_checkbox.assert_called_once()

        # Verificar que la estructura devuelta por build es un Container
        self.assertEqual(login_container.bgcolor, '#15191E')

    def test_login_action_success(self):
        # Configurar el valor devuelto por find_and_return_node como si el usuario fuera encontrado
        self.mock_backend.find_and_return_node.return_value = True

        # Llamar a LogInAction con valores válidos
        self.login_instance.LogInAction(dpi="123456789", admin_value=True)

        # Verificar que se haya asignado el dpi y se haya redirigido a /home
        self.assertEqual(self.login_instance.dpi, "123456789")
        self.mock_page.go.assert_called_with("/home")

    def test_login_action_failure(self):
        # Configurar el valor devuelto por find_and_return_node como si el usuario no fuera encontrado
        self.mock_backend.find_and_return_node.return_value = False

        # Llamar a LogInAction con un dpi inválido
        self.login_instance.LogInAction(dpi="987654321", admin_value=False)

        # Verificar que se haya mostrado el mensaje de error en el SnackBar
        self.mock_page.snack_bar.open = True
        self.mock_page.snack_bar.bgcolor = "red"
        self.mock_page.update.assert_called_once()


if __name__ == "__main__":
    unittest.main()
