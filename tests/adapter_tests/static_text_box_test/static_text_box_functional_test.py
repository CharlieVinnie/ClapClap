import adapter
from adapter import pygame_gui_testing # type: ignore
import threading
import pytest
from .controller.main_control import gameEntrance

@pytest.mark.parametrize("pygame_gui_testing", [gameEntrance], indirect=True)
def test_single_button(pygame_gui_testing: threading.Thread):

    button = adapter.findButton("#toggler_button")

    adapter.simulate_click_button(button)

    adapter.findTextbox("#first_text_box")

    adapter.simulate_click_button(button)

    with pytest.raises(adapter.ElementNotFoundError):
        adapter.findTextbox("#first_text_box")

    adapter.simulate_click_button(button)

    adapter.findTextbox("#first_text_box")
