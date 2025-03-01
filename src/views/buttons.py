from typing import Callable
import views


def createStartDummyButton(callback: Callable[[],None]):
    views.gui_object_list.append(views.MyButton("StartDummy", callback))