import adapter
import views.buttons
import views.images


def startDummy():
    print("Dummy!!")


def gameEntrance():
    def init():

        views.images.showEntranceBackground()

        views.buttons.createStartDummyButton(startDummy)

    adapter.start(init)


if __name__ == "__main__":
    gameEntrance()