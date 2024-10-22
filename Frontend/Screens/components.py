from flet import Text, alignment, margin, Container, TextField, TextStyle, ElevatedButton
from cerberus import Validator

# Validation function using Cerberus
def validate_input(data):
    schema = {'text': {'type': 'string', 'minlength': 1, 'maxlength': 100},
              'hide': {'type': 'boolean'},
              'width_par': {'type': 'integer', 'min': 1, 'max': 1000}}
    v = Validator(schema)
    if not v.validate(data):
        raise ValueError(f"Invalid input: {v.errors}")

# Modified input_text function with validation
def input_text(text: str, hide: bool, width_par: int):
    # Validate the input parameters
    validate_input({'text': text, 'hide': hide, 'width_par': width_par})

    # Proceed to create the TextField if validation passes
    return TextField(
        label=text,
        label_style=TextStyle(color='#666C75'),
        color='white',
        height=48,
        width=width_par,
        bgcolor='#1D242D',
        filled=True,
        border_color='#666C75',
        password=hide,
        can_reveal_password=hide
    )


def button(text: str):
    return Container(
        alignment=alignment.center,
        margin=margin.only(top=15),
        content=ElevatedButton(
            on_click=None,
            content=Text(
                text,
                size=15,
                weight='bold',
                color="white"
            ),
            height=48,
            width=180,
            bgcolor='blue'
        )
    )

