from pygame_gui.core import UIContainer
import typing
from .. import manager

class ButtonNotFoundError(Exception): pass

def findElement(name: str):
    try:
        assert manager is not None
        container = typing.cast( UIContainer, manager.get_root_container() )
        element = next( elem for elem in container.elements if elem.get_object_ids()[0] == name )
        return element
    except StopIteration:
        raise ButtonNotFoundError(f"element \"{name}\" not found")
