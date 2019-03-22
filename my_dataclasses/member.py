from dataclasses import dataclass, field, asdict


@dataclass(order=True)
class Member(object):
    name: str
    phone: str
    email: str
    year_of_birth: int = field(default_factory=int)

    def __post_init__(self):
        self.year_of_birth = int(self.year_of_birth)

    def get_dict(self):
        return asdict(self)

    def csv_repr(self):
        return self.get_dict()


if __name__ == "__main__":
    test = Member("asd", "asd", "asd", 5)
    print(test)
