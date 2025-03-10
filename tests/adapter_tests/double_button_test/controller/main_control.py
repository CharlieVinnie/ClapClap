import adapter
from ..views import buttons, images
import logging

logger = logging.getLogger()

other_on = False

def toggleOther():
    global other_on

    if other_on:
        buttons.removeOtherButton()
        other_on = False
    else:
        buttons.createOtherButton(lambda: logger.info("hello"))
        other_on = True


def gameEntrance():
    def init():

        images.showEntranceBackground()

        buttons.createStartDummyButton(toggleOther)

    adapter.start(init)


if __name__ == "__main__":
    gameEntrance()