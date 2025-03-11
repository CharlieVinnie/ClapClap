import adapter
from adapter import pygame_gui_testing # type: ignore
import threading
import pytest
from .controller.main_control import gameEntrance
import logging

@pytest.mark.parametrize("pygame_gui_testing", [gameEntrance], indirect=True)
def test_single_button(caplog: pytest.LogCaptureFixture, pygame_gui_testing: threading.Thread):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    button = adapter.findButton("#start_dummy_button")
    adapter.simulate_click_button(button)

    adapter.main.main_loop_event.wait()

    for handler in logger.handlers:
        handler.flush()
    
    assert "hello" in caplog.text
