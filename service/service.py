from typing import Callable, Dict
from my_dataclasses import Member, Sport, Plays
from repo import MemberRepo, RelationError, RepoFullError
from ui import Menu, UI


class Service(object):
    def __init__(self):
        self.__command_stack = list()
        self.__function_stack = list()
        self.ui = UI()
        self.member_repo = MemberRepo()
        self.__active = False

    def run(self):
        self.__active = True
        self.next(self.main_menu)
        while self.__function_stack and self.__active:
            function, arguments = self.__function_stack[-1]
            function(*arguments)

    def main_menu(self):
        options = {
            "Members": self.member_menu,
            "Sports": self.sport_menu,
            "Quit": self.quit
        }
        menu = Menu("Main menu", options)
        val, function = menu.get_input()
        self.next(function)

    def member_menu(self):
        options = {
            "See all members": self.all_members,
            "Search members": self.member_search,
            "Add new member": self.add_member,
            "Back": self.back
        }
        menu = Menu("Member menu", options)
        val, function = menu.get_input()
        self.next(function)

    def member_search(self):
        parameters = self.ui.search(Member)
        if not any(parameters.values()):
            self.back()
        results = self.member_repo.multi_field_search(parameters)
        if results:
            member = self.ui.search_result_choice(results)
            self.next(self.selected_member, member)
        else:
            self.back()

    def all_members(self):
        results = self.member_repo.get_all()
        if results:
            member, fun = self.ui.search_result_choice(
                results, self.selected_member, self.back
            )
            self.next(fun, member)
        else:
            self.back()

    def selected_member(self, member: Member, created=False):
        message = self.ui.get_info(member)
        options = {
            "Update this member": (self.update_member, [member]),
            "Delete this member": (self.delete_member, [member]),
            "See sports this member is member is registered in":
            (self.member_relation, [member]),
            "Back To Members": (self.member_menu,),
            "Undo" if created else "Back": (self.back, []),
        }
        menu = Menu(message, options)
        key, val = menu.get_input()
        self.next(*val)

    def add_member(self):
        new_member = self.ui.get_member()
        self.member_repo.add(new_member)
        self.add_command(self.member_repo.remove, new_member)
        self.__function_stack.pop()
        self.next(self.selected_member, new_member)

    def update_member(self, member):
        pass

    def delete_member(self, member):
        pass

    def member_relation(self, member):
        pass

    def sport_menu(self):
        pass

    def undo(self, *junk):
        methods = self.__command_stack.pop()
        for undo_method, arguments in reversed(methods):
            message = undo_method(*arguments)
            if message:
                Menu.global_message += str(message)

    def back(self, *junk):
        self.__function_stack.pop()
        self.__function_stack.pop()

    def add_command(self, function: Callable, *args):
        """Call after individual file-system changes."""
        try:
            self.__command_stack[-1].append((function, args))
        except IndexError:
            self.add_command_frame(function, *args)

    def next(self, function: Callable, *args):
        """Call this after every function, pointing to the next one."""
        Menu.global_message = ""
        # function(*args)
        self.__function_stack.append((function, args))

    def add_command_frame(self, function: Callable = None, *args):
        """Call for whole file-system transactions."""
        self.__command_stack.append(list())
        if function is not None:
            self.add_command(function, *args)

    def quit(self):
        self.__active = False
