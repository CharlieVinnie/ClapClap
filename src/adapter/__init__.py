import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def start():

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    pygame.display.set_caption("dummy qwq")

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255,255,255))

        pygame.draw.circle(screen, (0,0,255), (SCREEN_WIDTH//2,SCREEN_HEIGHT//2), 50)

        pygame.display.flip()

    pygame.quit()