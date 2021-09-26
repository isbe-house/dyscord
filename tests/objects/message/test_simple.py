import datetime

from src.simple_discord.objects import Message, Snowflake
from tests.objects.message import samples


def test_creation():
    obj = Message()
    assert type(obj) is Message


def test_simple_sample():
    obj = Message().from_dict(samples.short_message)

    assert obj.id == Snowflake('891001575697432586')
    assert type(obj.id) is Snowflake

    assert obj.channel_id == Snowflake('804392362629267458')
    assert type(obj.channel_id) is Snowflake

    assert obj.guild_id == Snowflake('804392362054910047')
    assert type(obj.guild_id) is Snowflake

    assert obj.content == 'test'
    assert type(obj.content) is str

    assert obj.timestamp == datetime.datetime.fromisoformat('2021-09-24T16:42:09.655000+00:00')
    assert type(obj.timestamp) is datetime.datetime

    assert obj.edited_timestamp is None

    assert obj.type == Message.MessageType.DEFAULT


def test_complex_samples():

    Message().from_dict(samples.short_message)
    Message().from_dict(samples.self_and_role_mention)
    Message().from_dict(samples.simple_message_update)
    Message().from_dict(samples.direct_message)
