from . import main
from typing import Any, Callable
import pygame_gui
from pygame_gui.elements import UIButton 
from pygame.event import Event

button_callback_map: dict[UIButton, Callable[[],None]] = {}


def create_button(callback: Callable[[],None], config: dict[str, Any]):
    print("create")

    button = UIButton(manager=main.manager, **config)

    button_callback_map[button] = callback

    print(len(button_callback_map))


def process_event(event: Event):

    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        print("I see:", button_callback_map)

        button = event.ui_element

        print(button)
        print(button_callback_map)

        if button in button_callback_map.keys():
            button_callback_map[button]()