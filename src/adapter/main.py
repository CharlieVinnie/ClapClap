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

started_condition = threading.Condition()

def start(init_function: Callable[[],None]):
    global manager, screen, started_condition
    
    with started_condition:
        try:

            pygame.init()

            screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

            pygame.display.set_caption("dummy qwq")

            manager = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT))

            init_function()

        finally:
            started_condition.notify_all()

    clock = pygame.time.Clock()
    running = True

    while running:

        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)

            buttons.process_event(event)

        manager.update(time_delta)
        screen.fill((0,0,0))
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()