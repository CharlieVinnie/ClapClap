from typing import Callable


class MyGuiObject:

    def __init__(self, name:str) -> None:
        self.name = name


class MyImage(MyGuiObject):

    def __init__(self, name: str) -> None:
        super().__init__(name)


class MyButton(MyGuiObject):

    def __init__(self, name: str, callback: Callable[[],None]) -> None:
        super().__init__(name)
        self.callback = callback


gui_object_list: list[MyGuiObject] = []