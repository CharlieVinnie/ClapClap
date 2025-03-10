import adapter
import threading
import pytest
from ..controller.main_control import gameEntrance
from adapter import pygame_gui_testing # type: ignore
# from ....testing.buttons import simulate_click_button
# import typing
# from pygame_gui.elements import UIButton

@pytest.mark.parametrize("pygame_gui_testing", [gameEntrance], indirect=True)
def test_double_button(caplog: pytest.LogCaptureFixture, pygame_gui_testing: threading.Thread):
    adapter.findElement("#start_dummy_button")
    # assert findElement("#start_dummy_button") is not None
    # dummy = typing.cast(UIButton, findElement("#start_dummy_button"))
    # simulate_click_button(dummy)
    # assert findElement("#start_dummy_button") is not None
