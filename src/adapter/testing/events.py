import pygame
from typing import Any, Callable
import threading

def postEvent(type: int, dict: dict[str, Any], callback: Callable[[],None]|None = None):

    wakeup_event = threading.Event()

    def after_process():
        if callback is not None:
            callback()
        wakeup_event.set()

    dict["post_process_callback"] = after_process

    pygame.event.post(pygame.event.Event(type,dict))

    wakeup_event.wait()