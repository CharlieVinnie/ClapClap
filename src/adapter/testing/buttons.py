import adapter
import adapter.testing
import adapter.testing.events
from pygame_gui.elements import UIButton
import pygame_gui

def simulate_click_button(button: UIButton):
    adapter.testing.events.postEvent(pygame_gui.UI_BUTTON_PRESSED,
                                     {"ui_element": button,})