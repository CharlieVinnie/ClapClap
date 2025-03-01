import views


def createStartDummyButton(callback: function):
    views.gui_object_list.append(views.MyButton("StartDummy", callback))