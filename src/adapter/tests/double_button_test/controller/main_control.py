from .... import main
import views.buttons
import views.images
import logging

logger = logging.getLogger()

other_on = False

def toggleOther():
    global other_on

    if other_on:
        views.buttons.removeOtherButton()
        other_on = False
    else:
        views.buttons.createOtherButton(lambda: logger.info("hello"))
        other_on = True


def gameEntrance():
    def init():

        views.images.showEntranceBackground()

        views.buttons.createStartDummyButton(toggleOther)

    print("hey there")

    main.start(init)


if __name__ == "__main__":
    gameEntrance()