import adapter
from ..views import buttons, textboxes

textbox_on = False

def toggleTextBox():
    global textbox_on

    if not textbox_on:
        textboxes.createFirstTextbox()
    else:
        textboxes.removeFirstTextbox()

def gameEntrance():
    def init():

        buttons.createTogglerButton(toggleTextBox)

    adapter.start(init)


if __name__ == "__main__":
    gameEntrance()