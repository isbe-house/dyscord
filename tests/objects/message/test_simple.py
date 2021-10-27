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

    for sample in samples.ALL:
        from pprint import pprint
        pprint(sample)
        message = Message()
        message.from_dict(sample)

        assert type(message.channel_id) is Snowflake
        assert type(message.id) is Snowflake

        assert isinstance(message.attachments, (list, type(None)))

        assert isinstance(message.author, (User, type(None)))

        assert isinstance(message.components, (list, type(None)))

        assert isinstance(message.content, (str, type(None)))

        assert isinstance(message.edited_timestamp, (datetime.datetime, type(None)))

        assert isinstance(message.embeds, (list, type(None)))

        assert isinstance(message.flags, (int, type(None)))

        assert isinstance(message.mention_everyone, (bool, type(None)))

        assert isinstance(message.mention_roles, (list, type(None)))

        assert isinstance(message.mentions, (list, type(None)))

        assert isinstance(message.pinned, (bool, type(None)))

        assert isinstance(message.timestamp, (datetime.datetime, type(None)))

        assert isinstance(message.tts, (bool, type(None)))

        assert isinstance(message.type, (message.MESSAGE_TYPE, type(None)))
        if not isinstance(message.type, type(None)):
            assert message.type in message.MESSAGE_TYPE


def test_init():

    obj = Message('Hello world!')

    assert obj.content == 'Hello world!'
    assert obj.channel is None
    assert obj.guild is None

    assert isinstance(obj.to_sendable_dict(), dict)


def test_member_author_attrs():

    obj = Message().from_dict(samples.message_from_a_thread)

    assert obj.member.id == Snowflake('185846097284038656')
