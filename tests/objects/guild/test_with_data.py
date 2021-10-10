
from src.simple_discord.objects import Guild, Channel, snowflake

from . import samples


def test_guild_data_sets():

    g = Guild().from_dict(samples.my_test_server['d'])

    assert g.name == 'Bot Playground'
    assert len(g.channels) == 9
    for channel in g.channels:
        assert isinstance(channel, Channel)

    g = Guild().from_dict(samples.discord_dev_example)
    assert g.name == 'Mason\'s Test Server'
    assert g.id == snowflake.Snowflake('2909267986263572999')
    assert g.discovery_splash is None
    assert g.approximate_member_count == 2
    assert g.approximate_presence_count == 2

    g = Guild().from_dict(samples.partial_guild_object)
