from dataclasses import dataclass, field
from datetime import datetime


@dataclass(order=True, frozen=True)
class Member(object):
    name: str
    phone: str
    email: str
    year_of_birth: int
    age: int = field(hash=False, compare=False, default=0)

    def __post_init__(self):
        super().__setattr__('age', datetime.now().year - self.year_of_birth)


if __name__ == "__main__":
    test = Member("asd", "asd", "asd", 5)
    print(test)
