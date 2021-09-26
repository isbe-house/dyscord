import pytest

from src.simple_discord.objects.interactions import CommandStructure


def test_names():
    new_cmd = CommandStructure()
    new_cmd.generate(name='Fail', description='Not valid', type=CommandStructure.COMMAND_TYPE.CHAT_INPUT)
    with pytest.raises(ValueError):
        new_cmd.validate()
