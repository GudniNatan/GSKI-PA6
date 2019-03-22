from dataclasses import dataclass, field


@dataclass(order=True, frozen=True)
class Sport(object):
    name: str
