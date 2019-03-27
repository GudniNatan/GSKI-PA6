from typing import Callable, Dict
from my_dataclasses import Member, Sport, Plays
from repo import MemberRepo
from ui import Menu, UI


class Service(object):
    def __init__(self):
        self.__undo_stack = list()
        self.__menu_stack = list()
        self.ui = UI()
        self.member_repo = MemberRepo()

    def start(self):
        print("Program start!")
        self.main_menu()

    def main_menu(self):
        self.__menu_stack.append((self.main_menu, []))
        options = {
            "Members": self.member_menu,
            "Sports": self.sport_menu,
            "Undo last operation": self.undo,
            "Quit": False
        }
        menu = Menu("Main menu", options)
        val, function = menu.get_input()
        if function:
            function()

    def member_menu(self):
        self.__menu_stack.append((self.member_menu, []))
        options = {
            "Search members": self.member_search,
            "Add new member": self.add_member,
            "Undo last operation": self.undo,
            "Back": self.back
        }
        menu = Menu("Member menu", options)
        val, function = menu.get_input()
        function()

    def member_search(self):
        self.__menu_stack.append((self.member_search, []))
        parameters = self.ui.search(Member)
        if not any(parameters.values()):
            self.back()
        results = self.member_repo.multi_field_search(parameters)
        if results:
            member = self.ui.search_result_choice(results)
            self.selected_member(member)
        else:
            self.back()

    def selected_member(self, member):
        self.__menu_stack.append((self.member_search, [member]))
        message = self.ui.get_info(member)
        options = {
            "Update this member": (self.update_member, [member]),
            "Delete this member": (self.delete_member, [member]),
            "See sports this member is member is registered in":
            (self.member_relation, [member]),
            "Undo last operation": (self.undo, []),
            "Back": (self.back, [])
        }
        menu = Menu(message, options)
        key, val = menu.get_input()
        val[0](*val[1])

    def add_member(self, member):
        pass

    def update_member(self, member):
        pass

    def delete_member(self, member):
        pass

    def member_relation(self, member):
        pass

    def sport_menu(self):
        pass

    def undo(self):
        function, kwargs = self.__undo_stack.pop()
        function(**kwargs)

    def back(self):
        self.__menu_stack.pop()
        function, args = self.__menu_stack.pop()
        function(*args)

    def add_undo_function(self, function: Callable, kwargs: Dict):
        self.__undo_stack.append((function, kwargs))
