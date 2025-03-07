import threading
# import pygame
import pytest
from ..controller.main_control import gameEntrance
from ....testing.fixture import pygame_gui_testing # type: ignore

@pytest.mark.parametrize("pygame_gui_testing", [gameEntrance], indirect=True)
def test_double_button(caplog: pytest.LogCaptureFixture, pygame_gui_testing: threading.Thread):
    print("hello")
