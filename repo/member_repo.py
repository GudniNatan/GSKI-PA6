from repo.repo import Repo, RelationError
from my_dataclasses import Member


class MemberRepo(Repo):
    def __init__(self, plays_repo=None):
        self.plays_repo = plays_repo
        return super().__init__(Member)

    def remove(self, instance):
        """Remove a member, and all associations of that member."""
        results = self.plays_repo.search("member", instance)
        for item in list(results):
            self.plays_repo.remove(item)
        return super().remove(instance)
