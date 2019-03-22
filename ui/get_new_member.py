from my_dataclasses import Member


def get_new_member():
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    year_of_birth = None
    while year_of_birth is None:
        try:
            year_of_birth = int(input("Year of birth: "))
        except ValueError:
            print("Year of birth should be a number.")
    return Member(name, phone, email, year_of_birth)
