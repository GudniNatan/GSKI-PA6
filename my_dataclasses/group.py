from dataclasses import dataclass
from my_dataclasses.sport import Sport


@dataclass(order=True, frozen=True)
class Group(object):
    sport: Sport
    age_from: int
    age_to: int
    max_size: int
