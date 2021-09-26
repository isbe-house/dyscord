from src.simple_discord.utilities import Cache


def test_simple_cache():
    x = Cache()
    y = Cache()

    assert x is not y
    assert id(x.guilds) == id(y.guilds)
    assert id(x.channels) == id(y.channels)
    assert id(x.users) == id(y.users)
