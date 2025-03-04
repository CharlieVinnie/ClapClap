import adapter
from typing import Any, Callable
import pygame_gui
from pygame_gui.elements import UIButton 
from pygame.event import Event

button_callback_map: dict[UIButton, Callable[[],None]] = {}


def create_button(callback: Callable[[],None], config: dict[str, Any]):

    button = UIButton(manager=adapter.manager, **config)

    button_callback_map[button] = callback


def process_event(event: Event):

    if event.type == pygame_gui.UI_BUTTON_PRESSED:

        button = event.ui_element

        if button in button_callback_map.keys():
            button_callback_map[button]()