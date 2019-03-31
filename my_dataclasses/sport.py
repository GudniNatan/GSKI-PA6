from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Sport(object):
    name: str
