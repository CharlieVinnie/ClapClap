from pygame_gui.elements import UIButton
import pyautogui
from pygame import Rect
import typing

def simulate_click_button(button: UIButton):
    rect = typing.cast(Rect, button.rect) # type: ignore
    x,y = rect.center
    pyautogui.click(x,y) # type: ignore