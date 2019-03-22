from typing import Callable, Dict
from service import MemberService, SportService


class Service(object):
    def __init__(self):
        self.__undo_stack = list()
        self.__menu_stack = list()

    def undo(self):
        function, kwargs = self.__undo_stack.pop()
        function(**kwargs)

    def add_undo_function(self, function: Callable, kwargs: Dict):
        self.__undo_stack.append((command, kwargs))
