from src.simple_discord.objects import Channel


def test_basic_channel():

    x = Channel()

    assert type(x) is Channel
