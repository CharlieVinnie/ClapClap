import adapter
import threading
import pytest
from .controller.main_control import gameEntrance
from adapter import pygame_gui_testing # type: ignore
import logging

@pytest.mark.parametrize("pygame_gui_testing", [gameEntrance], indirect=True)
def test_double_button(caplog: pytest.LogCaptureFixture, pygame_gui_testing: threading.Thread):
    caplog.set_level(logging.INFO)

    dummy_button = adapter.findButton("#start_dummy_button")

    adapter.simulate_click_button(dummy_button)

    other_button = adapter.findButton("#other_button")

    adapter.simulate_click_button(other_button)

    assert caplog.text.count("hello") == 1

    adapter.simulate_click_button(other_button)

    assert caplog.text.count("hello") == 2

    adapter.simulate_click_button(dummy_button)

    with pytest.raises(adapter.ElementNotFoundError):
        adapter.findElement("#other_button")
    
    adapter.simulate_click_button(dummy_button)

    other_button = adapter.findButton("#other_button")

    adapter.simulate_click_button(other_button)

    assert caplog.text.count("hello") == 3