import datetime

from src.dyscord.objects import Message, Snowflake, User
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

    assert obj.type == Message.MESSAGE_TYPE.DEFAULT


def test_complex_samples():

    key_finder = None
    for sample in samples.ALL:
        if key_finder is None:
            key_finder = set(sample.keys())
            continue
        key_finder = key_finder.intersection(set(sample.keys()))
    print('All messages have the following:')
    print(key_finder)

    for sample in samples.ALL:
        message = Message()
        message.from_dict(sample)

        assert hasattr(message, 'attachments')
        assert type(message.attachments) is list

        assert hasattr(message, 'author')
        assert type(message.author) is User

        assert hasattr(message, 'channel_id')
        assert type(message.channel_id) is Snowflake

        assert hasattr(message, 'components')
        assert type(message.components) is list

        assert hasattr(message, 'content')
        assert type(message.content) is str

        assert hasattr(message, 'edited_timestamp')
        assert (type(message.edited_timestamp) is datetime.datetime) or (message.edited_timestamp is None)

        assert hasattr(message, 'embeds')
        assert type(message.embeds) is list

        assert hasattr(message, 'flags')
        assert type(message.flags) is int

        assert hasattr(message, 'id')
        assert type(message.id) is Snowflake

        assert hasattr(message, 'mention_everyone')
        assert type(message.mention_everyone) is bool

        assert hasattr(message, 'mention_roles')
        assert type(message.mention_roles) is list

        assert hasattr(message, 'mentions')
        assert type(message.mentions) is list

        assert hasattr(message, 'pinned')
        assert type(message.pinned) is bool

        assert hasattr(message, 'timestamp')
        assert type(message.timestamp) is datetime.datetime

        assert hasattr(message, 'tts')
        assert type(message.tts) is bool

        assert hasattr(message, 'type')
        assert type(message.type) is message.MESSAGE_TYPE
        assert message.type in message.MESSAGE_TYPE


def test_complex_properties():
    pass
