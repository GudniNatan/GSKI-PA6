from typing import Callable, Dict
from my_dataclasses import Member, Sport, Plays
from repo import MemberRepo, RelationError, RepoFullError, SportRepo
from repo import PlaysRepo, Repo, GroupRepo, GroupMemberRepo
from ui import Menu, UI


class Service(object):
    def __init__(self):
        self.__command_stack = list()
        self.__function_stack = list()
        self.ui = UI()
        self.member_repo = MemberRepo()
        self.sport_repo = SportRepo()
        self.plays_repo = PlaysRepo(self.member_repo, self.sport_repo)
        self.group_repo = GroupRepo(self.sport_repo)
        self.group_member_repo = GroupMemberRepo(
            self.group_repo, self.member_repo
        )
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
            "Back": self.back,
            "Save & Quit": self.quit
        }
        menu = Menu("Main menu", options)
        val, function = menu.get_input()
        self.next(function)

    def member_menu(self, message=""):
        options = {
            "See all members": self.order_members,
            "Search members": self.member_search,
            "Add new member": self.add_member,
            "Go to main menu": self.main_menu,
            "Back": self.back
        }
        menu = Menu(message + "Member menu", options)
        val, function = menu.get_input()
        self.next(function)

    def member_search(self):
        parameters = self.ui.search(Member)
        return self.search_results(self.member_repo, parameters)

    def order_members(self):
        options = {
            "Name": (self.all_members, "name"),
            "Phone": (self.all_members, "phone"),
            "Email": (self.all_members, "email"),
            "Year of birth": (self.all_members, "year_of_birth"),
            "Age": (self.all_members, "age"),
            "Registered sports": (self.all_members, "sports"),
            "Back": (self.back,)
        }
        menu = Menu("Order by", options)
        name, val = menu.get_input()
        self.next(*val)

    def all_members(self, order_by="name"):
        return self.search_results(self.member_repo, self.selected_member,
                                   order_by=order_by)

    def search_results(self, repo: Repo, next_funct,
                       parameters=None, order_by=""):
        if parameters is None:
            if not order_by:
                results = repo.get_all()
            else:
                results = repo.order_by(order_by)
        elif not any(parameters.values()):
            self.__function_stack.pop()
            Menu.global_message = "Returned as no parameters were input\n"
            return
        else:
            results = repo.multi_field_search(parameters)
        if results:
            choice, funct = self.ui.search_result_choice(
                results, next_funct, self.back
            )
            self.next(funct, choice)
        else:
            Menu.global_message = "No results found\n"
            self.__function_stack.pop()

    def selected_member(self, member: Member, update=False, update_message=""):
        message = self.ui.get_info(member)
        options = {
            "Update this member": (self.update_member, member),
            "Delete this member": (self.delete_member, member),
            "See sports this member is registered in":
            (self.member_sports, member),
            "See groups this member is registered in":
            (self.member_groups, member),
            "Register this member for a sport":
            (self.register_member, member),
            "Register this member for a group in registered sport":
            (self.register_for_group, member),
            "Go to Member menu": (self.member_menu,),
            "Undo" if update else "Back": (self.back,),
            "Unregister this member from a sport":
            (self.unregister_member, member),
            "Unregister this member from a sport group":
            (self.unregister_group_member, member),
        }
        menu = Menu(update_message + message, options)
        key, val = menu.get_input()
        self.next(*val)

    def add_member(self):
        self.__function_stack.pop()
        new_member = self.ui.get_member()
        result_msg, rev_function, member = self.member_repo.add(new_member)[0]
        self.add_command_frame(rev_function, member)
        self.next(self.selected_member, new_member, True, result_msg)

    def update_member(self, member):
        updated_member = self.ui.update_member(member)
        return self.update_item(member, updated_member,
                                self.member_repo, self.selected_member)

    def delete_member(self, member):
        result_msg = self.delete_repo_item(member, self.member_repo)
        self.next(self.member_menu, result_msg)

    def update_item(self, old_item, new_item, repo: Repo, next_funct):
        self.__function_stack.pop()
        results = repo.update(old_item, new_item)
        self.add_command_frame()
        result_msg = ""
        for result in results:
            msg, fun, effected_item = result
            result_msg += msg
            self.add_command(fun, effected_item)
        self.next(next_funct, new_item, True, result_msg)

    def delete_repo_item(self, item, repo: Repo):
        self.__function_stack.pop()
        delete_results = repo.remove(item)
        self.add_command_frame()
        result_msg = ""
        for result in delete_results:
            msg, fun, effected_item = result
            self.add_command_frame(repo.add, item)
            result_msg += msg
        return result_msg

    def member_sports(self, member):
        """Get all Sports related to this member."""
        return self.search_results(self.plays_repo, self.selected_sport,
                                   parameters={"member": member})

    def member_groups(self, member):
        """Get all Groups related to this member."""
        return self.search_results(
            self.group_member_repo, self.selected_group, {"member": member}
        )

    def register_member(self, member):
        self.__function_stack.pop()
        sport = self.ui.choose(self.sport_repo.get_all(),
                               "Choose a sport to register the member for:")
        result_msg, rev_function, plays = self.plays_repo.add(
            Plays(member, sport)
        )[0]
        self.add_command_frame(rev_function, member)
        self.next(self.selected_member, member, True, result_msg)

    def register_for_group(self, member):
        pass

    def unregister_group_member(self, member):
        pass

    def sport_menu(self, message=""):
        options = {
            "See all sports": (self.order_sports,),
            "Search sports": (self.sport_search,),
            "Add new sport": (self.add_sport,),
            "See sport groups": (self.search_results, self.group_repo, self.group_repo, None, "sport"),
            "Go to main menu": (self.main_menu,),
            "Back": (self.back,)
        }
        menu = Menu(message + "Sport menu", options)
        description, val = menu.get_input()
        self.next(*val)

    def order_sports(self):
        options = {
            "Name": (self.all_sports, "name"),
            "Registered members": (self.all_sports, "members"),
            "Back": (self.back,)
        }
        menu = Menu("Order by", options)
        name, val = menu.get_input()
        self.next(*val)

    def add_sport(self):
        self.__function_stack.pop()
        new_sport = self.ui.new_sport()
        result_msg, rev_function, sport = self.sport_repo.add(new_sport)[0]
        self.add_command_frame(rev_function, sport)
        self.next(self.selected_sport, new_sport, True, result_msg)

    def sport_search(self):
        parameters = self.ui.search(Sport)
        return self.search_results(self.sport_repo, self.selected_sport,
                                   parameters=parameters)

    def all_sports(self, order_by="name"):
        return self.search_results(self.sport_repo, self.selected_sport,
                                   order_by=order_by)

    def selected_sport(self, sport: Sport, update=False, update_message=""):
        message = self.ui.get_info(sport)
        options = {
            "Update this sport": (self.update_sport, sport),
            "Delete this sport": (self.delete_sport, sport),
            "See members registered for this sport":
            (self.sport_members, sport),
            "Go to Sport menu": (self.sport_menu,),
            "Undo" if update else "Back": (self.back,),
        }
        menu = Menu(update_message + message, options)
        key, val = menu.get_input()
        self.next(*val)

    def update_sport(self, sport):
        updated_sport = self.ui.new_sport()
        return self.update_item(sport, updated_sport,
                                self.sport_repo, self.selected_sport)

    def delete_sport(self, sport):
        result_msg = self.delete_repo_item(sport, self.sport_repo)
        self.next(self.sport_menu, result_msg)

    def sport_members(self, sport):
        """Get all Members related to this sport."""
        return self.search_results(self.plays_repo, self.selected_member,
                                   parameters={"sport": sport})

    def unregister_member(self, member):
        sport = self.ui.choose(
            self.plays_repo.search("member", member),
            "Choose a sport to unregister this member from:"
        )

    def undo(self, *junk):
        methods = self.__command_stack.pop()
        for undo_method, arguments in reversed(methods):
            message = undo_method(*arguments)
            if message:
                Menu.global_message += str(message)
        self.__function_stack.pop()

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
        self.__function_stack.append((self.undo, []))

    def quit(self):
        self.__active = False
