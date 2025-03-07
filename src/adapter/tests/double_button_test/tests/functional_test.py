import threading
# import pygame
import pytest
from adapter.tests.double_button_test.controller.main_control import gameEntrance

def test_double_button(caplog: pytest.LogCaptureFixture):
    main_thread = threading.Thread(target=gameEntrance)
    main_thread.start()