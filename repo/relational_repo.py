from sortedcontainers import SortedSet
from repo.repo import Repo, RelationError


class RelationalRepo(Repo):
    """This subtype of repo holds repos that link 2 other repos."""

    def search(self, field, key):
        results = super().search(field, key)
        other_field_set = SortedSet()
        other_field = None
        for a_field in self.dicts:
            if a_field != field:
                other_field = a_field
                break
        for result in results:
            other_field_set.add(getattr(result, other_field))
        return other_field_set
