from flet import Text, alignment, margin, Container, TextField, TextStyle, ElevatedButton

def input_text(text: str, hide: bool, width_par: int):
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
