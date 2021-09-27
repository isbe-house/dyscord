import pytest

from src.simple_discord.objects.interactions import Command, COMMAND_TYPE, COMMAND_OPTION


def test_bad_validations():
    new_cmd = Command()
    new_cmd.generate(name='Fail', description='Not valid', type=COMMAND_TYPE.CHAT_INPUT)
    with pytest.raises(ValueError):
        new_cmd.validate()

    new_cmd.generate(name='123123123412312312341231231234123', description='Not valid', type=COMMAND_TYPE.CHAT_INPUT)
    with pytest.raises(ValueError):
        new_cmd.validate()

    new_cmd.generate(name='good_name', description='x' * 101, type=COMMAND_TYPE.CHAT_INPUT)
    with pytest.raises(ValueError):
        new_cmd.validate()

    new_cmd.generate(name='good_name', description='Good description', type=1.0)  # type: ignore
    with pytest.raises(TypeError):
        new_cmd.validate()

    new_cmd.generate(name='good_name', description='Good description', type=1)  # type: ignore
    with pytest.raises(TypeError):
        new_cmd.validate()

    new_cmd.generate(name='good_name', description='Good description', type=1)  # type: ignore
    with pytest.raises(TypeError):
        new_cmd.validate()

    new_cmd.generate(name='good_name', description='Good description', type=COMMAND_TYPE.CHAT_INPUT, default_permission='Frog')  # type: ignore
    with pytest.raises(TypeError):
        new_cmd.validate()

    new_cmd.generate(name='good_name', description='Good description', type=COMMAND_TYPE.CHAT_INPUT, default_permission=1)  # type: ignore
    with pytest.raises(TypeError):
        new_cmd.validate()


def test_bad_options():
    new_cmd = Command()
    new_cmd.generate(name='good', description='Valid.', type=COMMAND_TYPE.CHAT_INPUT)

    # Add too many options
    for i in range(26):
        new_cmd.add_option_typed(COMMAND_OPTION.INTEGER, name='fail', description='Test')
    with pytest.raises(OverflowError):
        new_cmd.validate()

    new_cmd = Command()
    new_cmd.generate(name='good', description='Valid.', type=COMMAND_TYPE.CHAT_INPUT)

    # Add bad options
    new_cmd.options = []
    new_cmd.options.append({'this dict': 'fails'})  # type: ignore
    with pytest.raises(TypeError, match=r'dict'):
        new_cmd.validate()

    new_cmd = Command()
    new_cmd.generate(name='good', description='Valid.', type=COMMAND_TYPE.CHAT_INPUT)

    # Add bad options
    new_cmd.options = []
    new_cmd.options.append('This string fails')  # type: ignore
    with pytest.raises(TypeError, match=r'str'):
        new_cmd.validate()
