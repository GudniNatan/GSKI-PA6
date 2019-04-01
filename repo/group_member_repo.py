from collections import deque
from repo.repo import RelationError
from repo.relational_repo import RelationalRepo
from my_dataclasses import GroupMember


class GroupMemberRepo(RelationalRepo):
    def __init__(self, group_repo, member_repo):
        self.member_repo = member_repo
        self.group_repo = group_repo
        self.member_repo.group_member_repo = self
        self.group_repo.group_member_repo = self
        self.member_repo.reliant_repos.append(self)
        self.group_repo.reliant_repos.append(self)
        self.waiting_lists = dict()
        return super().__init__(GroupMember)

    def add(self, instance, *args):
        if instance.member not in self.member_repo:
            raise RelationError("Member does not exist")
        if instance.group not in self.group_repo:
            raise RelationError("Group does not exist")
        age = instance.member.age
        age_from = instance.group.age_from
        age_to = instance.group.age_to
        if age_from > age or age_to < age:
            raise RelationError(
                "ERROR: Member is not in the right " +
                "age range to join this group\n"
            )
        group_members = self.search("group", instance.group)
        if (len(group_members) >= instance.group.max_size
                and instance.member not in group_members):
            try:
                self.waiting_lists[instance.group].append(instance)
            except KeyError:
                self.waiting_lists[instance.group] = deque([instance])
            raise RelationError(
                f"NOTICE: This group can only have {instance.group.max_size}" +
                " members and is full. This member was instead added to the " +
                "waiting list to join this group.\n"
            )
        return super().add(instance, *args)

    def remove(self, instance, *args):
        result = super().remove(instance, *args)
        try:
            waiting_list = self.waiting_lists[instance.group]
        except KeyError:
            waiting_list = None
        if waiting_list:
            new_instance = waiting_list.popleft()
            msg, rev, item = self.add(new_instance)[0]
            msg = "A member in the waiting list was added to the group.\n"
            result = [(msg, rev, item)] + result
        return result
