from typing import Callable
from views import gui


def createStartDummyButton(callback: Callable[[],None]):
    gui.gui_object_list.append(gui.MyButton("StartDummy", callback))