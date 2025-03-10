import adapter
import adapter.buttons
from typing import Callable
import adapter.testing
import adapter.testing.findelem
import pygame

def createStartDummyButton(callback: Callable[[],None]):

    adapter.buttons.create_button(callback,
                                  config=
                                  { "object_id": "#start_dummy_button",
                                    "text": "Dummy",
                                    "relative_rect": pygame.Rect((100,100),(200,50)), } )


def createOtherButton(callback: Callable[[],None]):

    adapter.buttons.create_button(callback,
                                  config=
                                  { "object_id": "#other_button",
                                    "text": "Hello!",
                                    "relative_rect": pygame.Rect((500,500),(200,50)), } )

def removeOtherButton():
    
    button = adapter.testing.findelem.findElement("#other_button")
    button.kill()