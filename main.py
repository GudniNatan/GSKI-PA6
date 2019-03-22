from ui.car_rental_ui import CarRentalUI
from my_dataclasses import Member
from structures.stack import Stack
# sample


def callback(*args):
    print(args)


command_stack = Stack()
ui = CarRentalUI(callback, callback)
me = Member("Guðni", "1234564", "gudni@fakemail.com", 1998)
print(me.get_dict())
menu = ui.get_edit_menu(me, "Member", "Breyttu þessum meðlim", callback)
callback, result = menu.get_input()
me2 = Member(**result)
print(me2)
