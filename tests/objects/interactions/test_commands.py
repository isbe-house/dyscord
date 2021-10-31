import pytest

from src.dyscord.objects.interactions import Command

from ...fixtures import mock_api  # noqa: F401


def test_validate_commands(mock_api):  # noqa: F811
    pass


@pytest.mark.asyncio
async def test_register_commands(mock_api):  # noqa: F811
    mock_api.create_guild_application_command.return_value = 'foo'

    new_command = Command()
    new_command.generate(name='test', description='I don\' got one.', type=Command.COMMAND_TYPE.CHAT_INPUT)
    new_command.validate()

    await new_command.register_to_guild('1234')

    mock_api.create_guild_application_command.assert_called()
