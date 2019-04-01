from my_dataclasses import Member, Sport, Plays, Group, GroupMember
from ui import Menu
from repo.member_repo import MemberRepo
from repo.sport_repo import SportRepo
from repo.plays_repo import PlaysRepo
from ui import UI
from service.service import Service
from repo import GroupMemberRepo, GroupRepo


if __name__ == "__main__":
    service = Service()
    service.run()
