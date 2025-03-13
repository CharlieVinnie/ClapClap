import adapter
from typing import Any
from pygame_gui.elements import UITextBox

def create_textbox(config: dict[str, Any]):
    UITextBox(manager=adapter.main.manager, **config)