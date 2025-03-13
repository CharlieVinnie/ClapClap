import adapter
from typing import Callable
import pygame

def createTogglerButton(callback: Callable[[],None]):

    adapter.create_button(callback,
                          config=
                          {
                              "object_id": "#toggler_button",
                              "text": "Toggle Me",
                              "relative_rect": pygame.Rect((100,100),(200,50)),
                          })
