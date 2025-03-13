import adapter
import pygame

def createFirstTextbox():

    adapter.create_textbox(config=
                           {
                              "object_id": "#first_text_box",
                              "html_text": "I am a text box",
                              "relative_rect": pygame.Rect((500,500),(200,50)),
                           })

def removeFirstTextbox():

    textbox = adapter.findTextbox("#first_text_box")
    textbox.kill()