import datetime

from src.dyscord.objects import Message, Snowflake, User, Member, TextChannel, Role


def test_timestamp():

    now = datetime.datetime.now()

    flags = Message.formatter.TIMESTAMP_FLAGS

    obj = Message.formatter.timestamp(now, flags.SHORT_DATE)
    assert obj == f'<t:{int(now.timestamp())}:d>'

    obj = Message.formatter.timestamp(now, flags.SHORT_TIME)
    assert obj == f'<t:{int(now.timestamp())}:t>'

    obj = Message.formatter.timestamp(now, flags.DEFAULT)
    assert obj == f'<t:{int(now.timestamp())}:f>'

    obj = Message.formatter.timestamp(now, flags.SHORT_DATE_TIME)
    assert obj == f'<t:{int(now.timestamp())}:f>'

    obj = Message.formatter.timestamp(now, flags.LONG_DATE_TIME)
    assert obj == f'<t:{int(now.timestamp())}:F>'

    obj = Message.formatter.timestamp(now, flags.LONG_TIME)
    assert obj == f'<t:{int(now.timestamp())}:T>'

    obj = Message.formatter.timestamp(now, flags.LONG_DATE)
    assert obj == f'<t:{int(now.timestamp())}:D>'

    obj = Message.formatter.timestamp(now, flags.RELATIVE_TIME)
    assert obj == f'<t:{int(now.timestamp())}:R>'

    obj = Message.formatter.timestamp()
    assert isinstance(obj, str)


def test_user():
    snowflake = Snowflake('1234')

    user = User()
    user.id = snowflake

    member = Member()
    member.id = snowflake

    output = Message.formatter.user(snowflake)
    assert output == f'<@{snowflake}>'

    output = Message.formatter.user(user)
    assert output == f'<@{snowflake}>'

    output = Message.formatter.user(member)
    assert output == f'<@{snowflake}>'


def test_nickname():
    snowflake = Snowflake('1234')

    user = User()
    user.id = snowflake

    member = Member()
    member.id = snowflake

    output = Message.formatter.user_nickname(snowflake)
    assert output == f'<@!{snowflake}>'

    output = Message.formatter.user_nickname(user)
    assert output == f'<@!{snowflake}>'

    output = Message.formatter.user_nickname(member)
    assert output == f'<@!{snowflake}>'


def test_channel():
    snowflake = Snowflake('1234')

    channel = TextChannel()
    channel.id = snowflake

    output = Message.formatter.channel(snowflake)
    assert output == f'<#{snowflake}>'

    output = Message.formatter.channel(channel)
    assert output == f'<#{snowflake}>'


def test_role():
    snowflake = Snowflake('1234')

    role = Role()
    role.id = snowflake

    output = Message.formatter.role(snowflake)
    assert output == f'<@&{snowflake}>'

    output = Message.formatter.role(role)
    assert output == f'<@&{snowflake}>'
