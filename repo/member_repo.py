import json
import shelve
from repo.repo import Repo
from my_dataclasses import Member


class MemberRepo(Repo):
    __members = set()

    def _get_collection(self):
        return self.__members

    def save(self):
        with shelve.open('data/data') as db:
            db['members'] = self.__members

    def load(self):
        with shelve.open('data/data') as db:
            self.__members = db['members']

    def add(self, member: Member):
        self.__members.add(member)

    def remove(self, member: Member):
        self.__members.remove(member)

    def update(self, old_member: Member, new_member: Member):
        self.remove(old_member)
        self.add(new_member)

    def find(self, name: str = None, phone: str = None,
             email: str = None, year_of_birth: int = None):
        arguments = {"name": name, "phone": phone, "email": email,
                     "year_of_birth": year_of_birth}
        return self.search(Member, arguments, self.__members)

    def __del__(self):
        self.save()
