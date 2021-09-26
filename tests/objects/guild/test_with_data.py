
from src.simple_discord.objects import Guild, Channel

from . import samples


def test_guild_data_sets():

    g = Guild().from_dict(samples.my_test_server['d'])

    assert g.name == 'Bot Playground'
    assert len(g.channels) == 9
    for channel in g.channels:
        assert isinstance(channel, Channel)
