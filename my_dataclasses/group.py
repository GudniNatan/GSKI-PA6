from dataclasses import dataclass
from my_dataclasses.sport import Sport


@dataclass(order=True, frozen=True)
class Group(object):
    sport: Sport
    age_from: int
    age_to: int
    max_size: int

    def __post_init__(self):
        age_from = min(self.age_from, self.age_to)
        super().__setattr__('age_to', max(self.age_from, self.age_to))
        super().__setattr__('age_from', age_from)
