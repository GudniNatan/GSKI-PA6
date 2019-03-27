import os
from ui.readkey import readkey
from typing import Dict, Callable


class Menu(object):
    __MAX_OPTIONS = 8

    def __init__(self, message: str, options: Dict[str, Callable] = None):
        self.__message = message
        self.__options = list() if options is None else list(options.items())
        self.__page = 0

    def __str__(self):
        start = self.__page * self.__MAX_OPTIONS
        end = (self.__page + 1) * self.__MAX_OPTIONS
        pagecount = len(self.__options) // self.__MAX_OPTIONS
        string = self.__message + "\n"
        string += "\n".join((f"[{i + 1}]: {key}" for i, (key, value)
                             in enumerate(self.__options[start:end])))
        if pagecount > 0:
            string += "\n" + "[9] Prev page"
            string += "\n" + "[0] Next page"
            string += f"\nPage {self.__page} of {pagecount}"

        return string

    def __clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def get_input(self) -> Callable:
        pagecount = len(self.__options) // self.__MAX_OPTIONS
        val = None
        while val is None:
            self.__clear_screen()
            print(self)
            key = readkey()
            try:
                itemnumber = int(chr(key)) - 1
                if itemnumber == 8:
                    self.__page = (self.__page - 1) % pagecount
                elif itemnumber == -1:
                    self.__page = (self.__page + 1) % pagecount
                else:
                    itemnumber += self.__page * self.__MAX_OPTIONS
                    item_key, val = self.__options[itemnumber]
            except (IndexError, ValueError):
                pass
        return item_key, val
