from repo.repo import Repo, RelationError
from my_dataclasses import Plays


class PlaysRepo(Repo):
    def __init__(self, member_repo, sport_repo):
        self.member_repo = member_repo
        self.sport_repo = sport_repo
        self.member_repo.plays_repo = self
        self.sport_repo.plays_repo = self
        return super().__init__(Plays)

    def add(self, instance, *args):
        if instance.member not in self.member_repo:
            raise RelationError("Member does not exist")
        if instance.sport not in self.sport_repo:
            raise RelationError("Sport does not exist")
        super().add(instance, *args)
