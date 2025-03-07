import threading
import pygame
import pytest
from typing import Callable
import typing

@pytest.fixture
def pygame_gui_testing(request: pytest.FixtureRequest):
    entrance = typing.cast(Callable[[],None], request)

    main_thread = threading.Thread(target=entrance)
    main_thread.start()

    yield main_thread

    pygame.event.post(pygame.event.Event(pygame.QUIT))
