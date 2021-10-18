from datetime import datetime

from src.dyscord.objects.events.typing_start import TypingStart
from src.dyscord.objects import Snowflake, Member, User
from . import samples


def test_samples():

    for sample in samples.user_typing_samples:
        x = TypingStart()

        data = sample['d']
        x.from_dict(data)

        assert type(x) is TypingStart
        assert hasattr(x, 'channel_id')
        assert type(x.channel_id) is Snowflake
        assert hasattr(x, 'guild_id')
        assert type(x.guild_id) is Snowflake
        assert hasattr(x, 'user_id')
        assert type(x.user_id) is Snowflake
        assert hasattr(x, 'timestamp')
        assert isinstance(x.timestamp, datetime)
        assert hasattr(x, 'member')
        assert isinstance(x.member, Member)
        assert isinstance(x.member, User)
