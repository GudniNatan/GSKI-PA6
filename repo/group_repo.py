from repo.repo import Repo, RelationError
from my_dataclasses import Group


class GroupRepo(Repo):
    def __init__(self, sport_repo, group_member_repo=None):
        self.sport_repo = sport_repo
        self.sport_repo.group_repo = self
        self.group_member_repo = group_member_repo
        self.sport_repo.reliant_repos.append(self)
        return super().__init__(Group)

    def add(self, instance, *args):
        if instance.sport not in self.sport_repo:
            raise RelationError("Sport does not exist")
        return super().add(instance, *args)
