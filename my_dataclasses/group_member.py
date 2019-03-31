from dataclasses import dataclass
from my_dataclasses.member import Member
from my_dataclasses.group import Group


@dataclass(order=True, frozen=True)
class GroupMember(object):
    member: Member
    group: Group
