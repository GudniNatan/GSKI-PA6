from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Member(object):
    name: str
    phone: str
    email: str
    year_of_birth: int


if __name__ == "__main__":
    test = Member("asd", "asd", "asd", 5)
    print(test)
