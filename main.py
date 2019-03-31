from my_dataclasses import Member, Sport, Plays
from ui import Menu
from repo.member_repo import MemberRepo
from repo.sport_repo import SportRepo
from repo.plays_repo import PlaysRepo
from ui import UI
from service.service import Service
# sample


def callback1(*args):
    print(1)


def callback2(*args):
    print(2)


def test():
    # command_stack = Stack()
    # ui = CarRentalUI(callback, callback)
    me = Member("Guðni", "1234564", "gudni@fakemail.com", 1998)
    # print(me.get_dict())
    a = MemberRepo()
    a.clear()
    mem_a = Member("GuðniA", "1234564", "gudni@fakemail.com", 1998)
    mem_b = Member("GuðniB", "1234564", "gudni@fakemail.com", 1995)
    mem_c = Member("GuðniC", "weasd", "gudni@fakemail.com", 2014)
    mem_d = Member("GuðniD", "ewr", "gudni@ggdfg.com", 1938)
    mem_e = Member("GuðniE", "1234564", "gudni@fakedfgmail.com", 1998)
    results = a.add(mem_a, mem_b, mem_c, mem_d, mem_e)
    msg = "".join(result[0] for result in results)
    UI().operation_result(msg, callback1, callback2)

    b = SportRepo()
    b.clear()
    sport_a = Sport("Baseball")
    sport_b = Sport("Tennis")
    b.add(sport_a, sport_b)

    c = PlaysRepo(a, b)
    c.clear()
    plays_a = Plays(mem_a, sport_a)
    plays_b = Plays(mem_d, sport_a)
    plays_c = Plays(mem_a, sport_b)
    plays_d = Plays(mem_e, sport_a)
    c.add(plays_a, plays_b, plays_c, plays_d)
    for member in a.order_by('sports'):
        print(member)
    print(a.order_by("sports"))
    print(mem_a.age)
    input()

    # a.remove(mem_a)
    for play in c:
        print(play)
    a.save()

    # my_ui = UI()
    # item = my_ui.choose(a.order_by("phone"))
    # my_ui.view_info(item)
    # print(item)
    # print()
    # parameters = my_ui.search(Member)
    # item = my_ui.search_result_choice(a.multi_field_search(parameters))
    # print(item)


if __name__ == "__main__":
    test()
    service = Service()
    service.run()
