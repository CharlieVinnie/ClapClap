from .. import main
from pygame_gui.core import UIContainer
from pygame_gui.elements import UIButton, UITextBox
import typing

class ButtonNotFoundError(Exception): pass

def findElement(name: str):
    try:
        assert main.manager is not None
        container = typing.cast( UIContainer, main.manager.get_root_container() )
        element = next( elem for elem in container.elements if elem.get_object_ids()[0] == name )
        return element
    except StopIteration:
        raise ButtonNotFoundError(f"element \"{name}\" not found")

def findButton(name: str):
    button = findElement(name)
    return typing.cast(UIButton, button)

def findTextbox(name: str):
    button = findElement(name)
    return typing.cast(UITextBox, button)