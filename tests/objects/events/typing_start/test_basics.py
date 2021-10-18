from src.dyscord.objects.events.typing_start import TypingStart


def test_create():

    x = TypingStart()

    assert type(x) is TypingStart
    assert hasattr(x, 'channel_id')
    assert x.channel_id is None
    assert hasattr(x, 'guild_id')
    assert x.guild_id is None
    assert hasattr(x, 'user_id')
    assert x.user_id is None
    assert hasattr(x, 'timestamp')
    assert x.timestamp is None
    assert hasattr(x, 'member')
    assert x.member is None
