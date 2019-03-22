from dataclasses import dataclass, field


@dataclass(order=True)
class Sport(object):
    name: str
