import os
from ui.readkey import readkey
from typing import Dict, Callable


class Menu(object):
    def __init__(self, message: str, options: Dict[str, Callable] = None):
        self.__message = message
        self.__options = list() if options is None else list(options.items())

    def __str__(self):
        string = self.__message + "\n"
        string += "\n".join((f"[{i + 1}]: {key}" for i, (key, value)
                             in enumerate(self.__options)))
        return string

    def __clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def get_input(self) -> Callable:
        self.__clear_screen()
        print(self)
        key = readkey()
        callback = None
        while callback is None:
            try:
                val, callback = self.__options[int(chr(key)) - 1]
            except (IndexError, ValueError):
                key = readkey()
        return callback
