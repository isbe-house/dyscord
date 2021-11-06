
from src.dyscord.objects import Member, User

from . import samples


def test_member_merge():

    data = samples.short_message
    author = User().from_dict(data['author'])
    member = Member().from_dict(data['member'])
    member.update_from_user(author)
    print(member)

    data = samples.self_and_role_mention['member']

    demo_user = User()
    demo_user.bot = True
    demo_user.system = True
    demo_user.mfa_enabled = True
    demo_user.banner = '12345'
    demo_user.accent_color = 0xffffff
    demo_user.locale = 'us'
    demo_user.verified = True
    demo_user.email = 'me@example.com'
    demo_user.flags = 0
    demo_user.premium_type = 0

    member = Member().from_dict(data)
    member.update_from_user(demo_user)
