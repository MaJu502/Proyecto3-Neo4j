import unittest
from unittest.mock import patch
from Frontend.Screens import components

class TestComponents(unittest.TestCase):

    @patch("Frontend.Screens.components.TextField")
    @patch("Frontend.Screens.components.TextStyle")
    def test_input_text(self, mock_text_style, mock_text_field):
        # Test parameters
        text = "Test Label"
        hide = True
        width_par = 200

        # Call the function
        components.input_text(text, hide, width_par)

        # Verify that TextField was called with the expected parameters
        mock_text_field.assert_called_with(
            label=text,
            label_style=mock_text_style.return_value,
            color='white',
            height=48,
            width=width_par,
            bgcolor='#1D242D',
            filled=True,
            border_color='#666C75',
            password=hide,
            can_reveal_password=hide
        )

    @patch("Frontend.Screens.components.Container")
    @patch("Frontend.Screens.components.ElevatedButton")
    def test_button(self, mock_elevated_button, mock_container):
        # Test parameter
        text = "Click Me"

        # Call the function
        components.button(text)

        # Verify that ElevatedButton and Container were called with the expected parameters
        mock_elevated_button.assert_called_with(
            on_click=None,
            content=mock_elevated_button.call_args[1]['content'],
            height=48,
            width=180,
            bgcolor='blue'
        )

        mock_container.assert_called_with(
            alignment=mock_container.call_args[1]['alignment'],
            margin=mock_container.call_args[1]['margin'],
            content=mock_elevated_button.return_value
        )

if __name__ == "__main__":
    unittest.main()
