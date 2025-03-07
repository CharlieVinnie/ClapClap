import threading
import pygame
import pytest
from adapter.tests.double_button_test.controller.main_control import gameEntrance

@pytest.fixture
def pygame_gui_testing():
    main_thread = threading.Thread(target=gameEntrance)
    main_thread.start()

    yield main_thread

    pygame.event.post(pygame.event.Event(pygame.QUIT))



def test_double_button(caplog: pytest.LogCaptureFixture, pygame_gui_testing: threading.Thread):
    pass
