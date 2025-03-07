import threading
import logging
# import pygame
import pytest
from ..controller.main_control import gameEntrance
from ....testing.fixture import pygame_gui_testing # type: ignore

@pytest.mark.parametrize("pygame_gui_testing", [gameEntrance], indirect=True)
def test_double_button(caplog: pytest.LogCaptureFixture, pygame_gui_testing: threading.Thread):
    pass




def test_logging(caplog: pytest.LogCaptureFixture):
    logger = logging.getLogger()

    with caplog.at_level(logging.INFO):
        logger.info("hello")

    assert "hello" in caplog.text