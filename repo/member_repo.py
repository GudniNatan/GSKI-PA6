from repo.repo import Repo, RelationError
from my_dataclasses import Member
from collections import OrderedDict


class MemberRepo(Repo):
    def __init__(self, plays_repo=None, group_member_repo=None):
        self.plays_repo = plays_repo
        self.group_member_repo = group_member_repo
        return super().__init__(Member)

    def remove(self, instance):
        """Remove a member, and all associations of that member."""
        results = self.plays_repo.search("member", instance)
        undos = list()
        for item in list(results):
            undos.extend(self.plays_repo.remove(item))
        return super().remove(instance) + undos

    def order_by(self, field):
        if field == "sports":
            # O(n), maintains order
            sport_order = self.plays_repo.order_by("sport")
            member_dict = OrderedDict()
            for play in sport_order:
                if play.member not in member_dict:
                    member_dict[play.member] = None
            return list(member_dict.keys())
        return super().order_by(field)
