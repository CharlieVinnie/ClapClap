import adapter
import adapter.buttons
from views import gui
from typing import Callable
import pygame

def createStartDummyButton(callback: Callable[[],None]):

    gui.gui_object_list.append(gui.MyButton("StartDummy", callback))

    adapter.buttons.create_button(callback, text="Dummy", relative_rect=pygame.Rect((100,100),(200,50)))
