from pygame_gui.elements import UIButton
import pygame
import pygame_gui

def simulate_click_button(button: UIButton):
    event = pygame.event.Event(pygame_gui.UI_BUTTON_PRESSED,
                      {"ui_element": button,})
    pygame.event.post(event)