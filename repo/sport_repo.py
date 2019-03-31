from collections import OrderedDict
from repo.repo import Repo, RelationError
from my_dataclasses import Sport


class SportRepo(Repo):
    def __init__(self, plays_repo=None, group_repo=None):
        self.plays_repo = plays_repo
        self.group_repo = group_repo
        return super().__init__(Sport)

    def remove(self, instance):
        """Remove a member, and all associations of that member."""
        for item in self.plays_repo.search("sport", instance):
            self.plays_repo.remove(item)
        return super().remove(instance)

    def order_by(self, field):
        if field == "members":
            # O(n), maintains order
            sport_order = self.plays_repo.order_by("member")
            sport_dict = OrderedDict()
            for play in sport_order:
                if play.sport not in sport_dict:
                    sport_dict[play.sport] = None
            return list(sport_dict.keys())
        return super().order_by(field)
