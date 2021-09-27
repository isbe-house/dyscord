import pytest

from src.simple_discord.objects.interactions import Command


def test_names():
    new_cmd = Command()
    new_cmd.generate(name='Fail', description='Not valid', type=Command.COMMAND_TYPE.CHAT_INPUT)
    with pytest.raises(ValueError):
        new_cmd.validate()

    new_cmd.generate(name='123123123412312312341231231234123', description='Not valid', type=Command.COMMAND_TYPE.CHAT_INPUT)
    with pytest.raises(ValueError):
        new_cmd.validate()

