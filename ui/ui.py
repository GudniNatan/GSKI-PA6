import typing
from dataclasses import asdict, fields
from ui.menu import Menu
from my_dataclasses import Sport, Member, Plays


class UI(object):
    """Class for quick UI shortcuts."""

    def get_member(self):
        print("Enter member info:")
        name = input("Name: ")
        phone = input("Phone: ")
        email = input("Email: ")
        year_of_birth = None
        while year_of_birth is None:
            try:
                year_of_birth = int(input("Year of birth: "))
            except ValueError:
                print("Year of birth should be a number.")
        new_member = Member(name, phone, email, year_of_birth)
        print("New member:", new_member)
        return new_member

    def update_member(self, old_member):
        print(f"Update member {old_member}:")
        name = input(f"Old name: {old_member.name}\nNew name: ")
        phone = input(f"Old phone: {old_member.phone}\nNew phone: ")
        email = input(f"Old email: {old_member.name}\nNew email: ")
        print(f"Old year of birth: {old_member.year_of_birth}")
        year_of_birth = None
        while year_of_birth is None:
            try:
                year_of_birth = int(input("New year of birth: "))
            except ValueError:
                print("Year of birth should be a number.")
        new_member = Member(name, phone, email, year_of_birth)
        print("Updated member:", new_member, "\n")
        return new_member

    def new_sport(self):
        print("Create new member:")
        name = input("Name: ")
        new_sport = Sport(name)
        print("New sport:", new_sport, "\n")
        return new_sport

    def choose(self, items: typing.Iterable, message: str = None):
        """Let user pick from list, returns picked item."""
        options = {str(item): item for item in items}
        message = "Choose an item:\n" if message is None else message
        menu = Menu(message, options)
        item_str, item = menu.get_input()
        print()
        return item

    def view_info(self, dataclass_instance):
        print(self.get_info(dataclass_instance))

    def get_info(self, dataclass_instance) -> str:
        """Get a string with detailed info about this dataclass instance."""
        item = asdict(dataclass_instance)
        class_type = type(dataclass_instance)
        string = f"Detailed info for this {class_type.__name__}:\n"
        for key, value in item.items():
            string += "\n" + key + ": " + str(value)
        return string + "\n"

    def search(self, dataclass) -> dict:
        """Start a search for specific item, returns search parameters."""
        print(f"Search {dataclass.__name__} repository")
        print("Leave a field blank to not search with it")
        parameters = dict()
        for field in fields(dataclass):
            parameters[field.name] = input(field.name + ": ")
        print()
        return parameters

    def search_result_choice(self, results):
        """Get user choice from search results."""
        return self.choose(results, "Search results:")
