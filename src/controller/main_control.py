import views.buttons
import views.images


def startDummy():
    print("Dummy!!")


def gameEntrance():

    views.images.showEntranceBackground()

    views.buttons.createStartDummyButton(startDummy)