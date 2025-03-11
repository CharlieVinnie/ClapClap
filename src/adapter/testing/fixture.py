from .. import main
import threading
import pytest
from typing import Callable
import typing
import pygame

@pytest.fixture
def pygame_gui_testing(request: pytest.FixtureRequest):
    entrance = typing.cast(Callable[[],None], request.param)

    main_thread = threading.Thread(target=entrance)
    main_thread.start()

    main.started_event.wait()

    yield main_thread

    pygame.event.post(pygame.event.Event(pygame.QUIT))
