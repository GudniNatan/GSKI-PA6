from repo.repo import Repo, RelationError
from my_dataclasses import Sport


class SportRepo(Repo):
    def __init__(self, plays_repo=None):
        self.plays_repo = plays_repo
        return super().__init__(Sport)

    def remove(self, instance):
        """Remove a member, and all associations of that member."""
        for item in self.plays_repo.search("sport", instance):
            self.plays_repo.remove(item)
        return super().remove(instance)
