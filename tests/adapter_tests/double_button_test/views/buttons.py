import adapter
import typing
from typing import Callable
import pygame
from pygame_gui.core import UIContainer
from pygame_gui.elements import UIButton

class ButtonNotFoundError(Exception): pass

def findElement(name: str):
    try:
        assert adapter.main.manager is not None
        container = typing.cast(UIContainer, adapter.main.manager.get_root_container())
        element = next( elem for elem in container.elements if elem.get_object_ids()[0] == name )
        return element
    except StopIteration:
        raise ButtonNotFoundError(f"element \"{name}\" not found")

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
    
    button = typing.cast(UIButton, findElement("#other_button"))
    adapter.remove_button(button)
    button.kill()