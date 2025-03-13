from typing import Callable
import pygame
import pygame_gui
import pygame_gui.ui_manager
from . import buttons
import threading

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

manager: pygame_gui.UIManager|None = None
screen = None

started_event = threading.Event()

def reset():
    global manager, screen, started_event
    manager = None
    screen = None
    started_event = threading.Event()

def start(init_function: Callable[[],None]):
    global manager, screen
    
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    pygame.display.set_caption("dummy qwq")

    manager = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT))

    init_function()

    started_event.set()

    clock = pygame.time.Clock()
    running = True

    while running:

        time_delta = clock.tick(60) / 1000.0

        post_process_callback_list: list[Callable[[],None]] = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)

            buttons.process_event(event)

            if hasattr(event, "post_process_callback"):
                post_process_callback_list.append(event.post_process_callback)

        manager.update(time_delta)
        screen.fill((0,0,0))
        manager.draw_ui(screen)

        pygame.display.flip()

        for callback in post_process_callback_list:
            callback()

    pygame.quit()