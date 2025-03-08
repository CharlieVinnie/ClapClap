from .... import main, buttons
from typing import Callable
import pygame
from pygame_gui.core import UIContainer

class ButtonNotFoundError(Exception): pass

def findElement(name: str):
    try:
        container: UIContainer = main.manager.get_root_container() # type: ignore
        element = next( elem for elem in container.elements if elem.get_object_ids()[0] == name )
        return element
    except StopIteration:
        raise ButtonNotFoundError(f"element \"{name}\" not found")

def createStartDummyButton(callback: Callable[[],None]):

    buttons.create_button(callback,
                                  config=
                                  { "object_id": "#start_dummy_button",
                                    "text": "Dummy",
                                    "relative_rect": pygame.Rect((100,100),(200,50)), } )


def createOtherButton(callback: Callable[[],None]):

    buttons.create_button(callback,
                                  config=
                                  { "object_id": "#other_button",
                                    "text": "Hello!",
                                    "relative_rect": pygame.Rect((500,500),(200,50)), } )

def removeOtherButton():
    
    button = findElement("#other_button")
    button.kill()