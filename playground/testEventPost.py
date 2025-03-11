import pygame
import threading
import time
import sys

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))

# Define a custom event type
MY_EVENT = pygame.USEREVENT + 1

def post_event():
    while True:
        time.sleep(1)
        event = pygame.event.Event(MY_EVENT, message="Posted from thread")
        pygame.event.post(event)

# Start a background thread
thread = threading.Thread(target=post_event, daemon=True)
thread.start()

# Event loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MY_EVENT:
            print(f"Received custom event: {event.message}")

pygame.quit()
sys.exit()
