import os
from ui.readkey import readkey
from typing import Dict, Callable


class Menu(object):
    def __init__(self, message: str, options: Dict[str, Callable] = None):
        self.__message = message
        self.__options = list() if options is None else list(options.items())

    def __str__(self):
        string = self.__message + "\n"
        for i, (key, value) in enumerate(self.__options):
            string += f"[{i + 1}]: {key}\n"
        string += "\n"
        return string

    def __clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def get_input(self) -> Callable:
        self.__clear_screen()
        print(self)
        key = readkey()
        callback = None
        while callback is None:
            try:
                val, callback = self.__options[int(chr(key)) - 1]
            except IndexError:
                key = readkey()
        return callback
