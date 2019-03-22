from termcolor import colored
from ui.car_rental_ui import CarRentalUI
from my_dataclasses import Member
from structures.stack import Stack
from ui.menu_remake import Menu
from repo.member_repo import MemberRepo
# sample


def callback1(*args):
    print(1)


def callback2(*args):
    print(2)


# command_stack = Stack()
# ui = CarRentalUI(callback, callback)
# me = Member("Guðni", "1234564", "gudni@fakemail.com", 1998)
# print(me.get_dict())
# menu = ui.get_edit_menu(me, "Member", "Breyttu þessum meðlim", callback)
# callback, result = menu.get_input()
# me2 = Member(**result)
# print(me2)
a = MemberRepo()
a.add(Member("Guðni", "1234564", "gudni@fakemail.com", 1998))
a.add(Member("Guðni", "1234564", "gudni@fakemail.com", 1998))
a.add(Member("Guðni", "weasd", "gudni@fakemail.com", 1998))
a.add(Member("Guðni", "ewr", "gudni@ggdfg.com", 1998))
a.add(Member("Guðni", "1234564", "gudni@fakedfgmail.com", 1998))
pprint(a.find(name="Guðni"))
