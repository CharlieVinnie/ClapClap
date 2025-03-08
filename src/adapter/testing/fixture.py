import threading
import pytest
from typing import Callable
import typing
from .. import manager, started_condition
import pygame

@pytest.fixture
def pygame_gui_testing(request: pytest.FixtureRequest):
    entrance = typing.cast(Callable[[],None], request.param)

    print(entrance)

    main_thread = threading.Thread(target=entrance)
    main_thread.start()

    with started_condition:
        started_condition.wait_for(lambda: manager is not None)

    print("hello")

    yield main_thread

    pygame.event.post(pygame.event.Event(pygame.QUIT))
