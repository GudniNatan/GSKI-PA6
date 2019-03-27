from dataclasses import dataclass
from my_dataclasses.member import Member
from my_dataclasses.sport import Sport


@dataclass(order=True, frozen=True)
class Plays(object):
    member: Member
    sport: Sport
