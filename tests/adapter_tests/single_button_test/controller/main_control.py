import adapter
from ..views import buttons
import logging

logger = logging.getLogger()

def gameEntrance():
    def init():

        buttons.createStartDummyButton(lambda: logger.info("hello"))

    adapter.start(init)


if __name__ == "__main__":
    gameEntrance()