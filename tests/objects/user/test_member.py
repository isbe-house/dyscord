
from src.simple_discord.objects import Member, User

from . import samples


def test_member_merge():

    data = samples.short_message
    author = User().from_dict(data['author'])
    member = Member().from_dict(data['member'])
    member.update_from_user(author)
    print(member)
    # assert False
