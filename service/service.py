from ui.car_rental_ui import CarRentalUI
from my_dataclasses import Member

# sample


def callback(*args):
    print("submitted")


ui = CarRentalUI()
me = Member("Guðni", "1234564", "gudni@fakemail.com")
ui.get_edit_menu(me, "Member", "Breyttu þessum meðlim", callback)
