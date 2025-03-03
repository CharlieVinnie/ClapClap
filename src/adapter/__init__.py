from typing import Callable
import pygame
import pygame_gui
import pygame_gui.ui_manager

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

manager = None
screen = None

def start(init_function: Callable[[],None]):

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    pygame.display.set_caption("dummy qwq")

    manager = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT))

    init_function()

    clock = pygame.time.Clock()
    running = True

    while running:

        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)
        
        screen.fill((255,255,255))

        pygame.draw.circle(screen, (0,0,255), (SCREEN_WIDTH//2,SCREEN_HEIGHT//2), 50)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()