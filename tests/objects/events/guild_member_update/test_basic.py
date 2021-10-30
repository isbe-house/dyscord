from src.dyscord.objects.events import GuildMemberUpdate

from . import samples


def test_instance():

    obj = GuildMemberUpdate()
    assert isinstance(obj, GuildMemberUpdate)


def test_raw_samples():

    for sample in samples.raw_guild_member_update_samples:
        data = sample['d']
        obj = GuildMemberUpdate(data)
        for key in data:
            assert hasattr(obj, key)
            assert (getattr(obj, key) is not None) or data[key] is None
