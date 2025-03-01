import adapter
import views.buttons
import views.images


def startDummy():
    print("Dummy!!")


def gameEntrance():

    adapter.start()

    views.images.showEntranceBackground()

    views.buttons.createStartDummyButton(startDummy)

if __name__ == "__main__":
    gameEntrance()