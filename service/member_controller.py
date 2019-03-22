from service.controller import Controller
from my_dataclasses import Member
from repo import MemberRepo
from ui import Menu, get_new_member


class MemberController(Controller):
    __members = MemberRepo()

    def add(self):
        new_member = get_new_member()
        self.__members.add(new_member)
        self.__service.add_undo_function(
            self.__members.remove, {"member": new_member}
        )

    def update(self, old_member):
        new_member = get_new_member()
        self.__members.update(old_member, new_member)
        self.__service.add_undo_function(
            self.__members.update,
            {"old_member": new_member, "new_member": old_member}
        )

    def delete_member(self, member):
        self.__members.remove(member)
        self.__service.add_undo_function(
            self.__members.add, {"member": member}
        )
