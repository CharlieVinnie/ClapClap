import adapter
from ..views import buttons, textboxes

textbox_on = False

def toggleTextBox():
    global textbox_on

    if not textbox_on:
        textboxes.createFirstTextbox()
        textbox_on = True
    else:
        textboxes.removeFirstTextbox()
        textbox_on = False

def gameEntrance():
    def init():

        buttons.createTogglerButton(toggleTextBox)

    adapter.start(init)


if __name__ == "__main__":
    gameEntrance()