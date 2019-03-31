from repo.repo import RelationError
from repo.relational_repo import RelationalRepo
from my_dataclasses import GroupMember


class GroupMemberRepo(RelationalRepo):
    def __init__(self, group_repo, member_repo):
        self.member_repo = member_repo
        self.group_repo = group_repo
        self.member_repo.group_member_repo = self
        self.group_repo.group_member_repo = self
        return super().__init__(GroupMember)

    def add(self, instance, *args):
        if instance.member not in self.member_repo:
            raise RelationError("Member does not exist")
        if instance.group not in self.group_repo:
            raise RelationError("Group does not exist")
        age = instance.member.age
        age_from = instance.group.age_from
        age_to = instance.group.age_to
        if age_from < age or age_to > age:
            raise RelationError("Member is not in the right age range to join")
        return super().add(instance, *args)
