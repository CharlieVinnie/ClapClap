import adapter
import typing
from typing import Callable
import pygame
from pygame_gui.elements import UIButton

class ButtonNotFoundError(Exception): pass

def createStartDummyButton(callback: Callable[[],None]):

    adapter.create_button(callback,
                                  config=
                                  { "object_id": "#start_dummy_button",
                                    "text": "Dummy",
                                    "relative_rect": pygame.Rect((100,100),(200,50)), } )


def createOtherButton(callback: Callable[[],None]):

    adapter.create_button(callback,
                                  config=
                                  { "object_id": "#other_button",
                                    "text": "Hello!",
                                    "relative_rect": pygame.Rect((500,500),(200,50)), } )

def removeOtherButton():
    
    button = typing.cast(UIButton, adapter.findElement("#other_button"))
    adapter.remove_button(button)
    button.kill()