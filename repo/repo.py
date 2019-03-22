from dataclasses import dataclass, field
from my_dataclasses import Member, Sport


@dataclass
class Repo(object):
    members: str
