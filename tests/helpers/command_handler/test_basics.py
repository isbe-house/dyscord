from unittest.mock import AsyncMock, MagicMock
import pytest
import httpx
from datetime import datetime, timedelta
from unittest.mock import Mock
from cachetools import TTLCache

from src.dyscord.client import DiscordClient
from src.dyscord.helper import CommandHandler
from src.dyscord.objects import Snowflake, Guild
from src.dyscord.objects.interactions import Interaction, InteractionData

from ...fixtures import mock_api  # noqa: F401


@pytest.fixture
def command_handler():
    x = CommandHandler
    x.registered_commands = dict()
    x.global_lookup = dict()
    x.guild_lookup = dict()
    x.registered_custom_ids = TTLCache(
        maxsize=float('inf'),
        ttl=timedelta(minutes=15),  # type: ignore
        timer=datetime.now,  # type: ignore
    )
    yield x


def test_create(command_handler):
    x = command_handler()
    assert x is not None


@pytest.mark.asyncio
async def test_register_global_callback(command_handler):

    async def callback_3(first, second, third):
        pass

    mock_str = Mock(str)
    mock_func = Mock(wraps=callback_3)
    mock_id = Mock(Snowflake)

    command_handler.register_global_callback(mock_str, mock_func, mock_id)
    print(command_handler.registered_commands)

    assert mock_str in command_handler.global_lookup
    assert mock_id in command_handler.registered_commands


@pytest.mark.asyncio
async def test_register_guild_callback(command_handler):

    async def callback_3(first, second, third):
        pass

    mock_str = Mock(str)
    mock_func = Mock(wraps=callback_3)
    mock_id = Mock(Snowflake)

    command_handler.register_guild_callback(mock_str, mock_func, mock_id, mock_id)
    print(command_handler.registered_commands)

    assert (mock_str, mock_id) in command_handler.guild_lookup
    assert mock_id in command_handler.registered_commands

    mock_guild = Mock(Guild)
    command_handler.register_guild_callback(mock_str, mock_func, mock_guild, mock_id)


@pytest.mark.asyncio
async def test_register_interaction_custom_id(command_handler):

    async def callback_3(first, second, third):
        pass

    mock_func = Mock(wraps=callback_3)
    mock_id = Mock(Snowflake)

    command_handler.register_interaction_custom_id(mock_id, mock_func, False)
    print(command_handler.registered_commands)

    assert mock_id in command_handler.registered_custom_ids

    command_handler.unregister_interaction_custom_id(mock_id)

    assert mock_id not in command_handler.registered_custom_ids

    with pytest.raises(KeyError):
        command_handler.unregister_interaction_custom_id(mock_id)


@pytest.mark.asyncio
async def test_handle_application_command(command_handler, mock_api):  # noqa: F811
    mock_api.get_global_application_command = AsyncMock(side_effect=httpx.HTTPStatusError('This failed', request=None, response=None))
    mock_api.get_guild_application_command = AsyncMock(side_effect=httpx.HTTPStatusError('This failed', request=None, response=None))

    mock_id = Mock(Snowflake)

    mock_client = Mock(DiscordClient)
    mock_interaction = Mock(Interaction)

    mock_interaction.data = Mock(InteractionData)
    mock_interaction.data.name = 'test'
    mock_interaction.data.id = mock_id

    with pytest.raises(LookupError):
        await command_handler.handle_application_command(mock_interaction, {}, mock_client)

    mock_interaction.guild_id = Mock(Snowflake)

    assert isinstance(mock_interaction.guild_id, Snowflake)

    with pytest.raises(LookupError):
        await command_handler.handle_application_command(mock_interaction, {}, mock_client)


@pytest.mark.asyncio
async def test_handle_registered_global_application_command(command_handler, mock_api):  # noqa: F811

    results_mock = MagicMock()
    d = {'name': 'test'}
    results_mock.__getitem__.side_effect = d.__getitem__

    assert results_mock['name'] == 'test'

    mock_api.get_global_application_command = AsyncMock(return_value=results_mock)
    mock_api.get_guild_application_command = AsyncMock(side_effect=httpx.HTTPStatusError('This failed', request=None, response=None))

    mock_func = AsyncMock()

    async def callback_2(first, second):
        await mock_func()

    mock_id = Mock(Snowflake)

    mock_client = Mock(DiscordClient)
    mock_interaction = Mock(Interaction)

    mock_interaction.data = Mock(InteractionData)
    mock_interaction.data.name = 'test'
    mock_interaction.data.id = mock_id

    command_handler.register_global_callback(mock_interaction.data.name, callback_2)

    await command_handler.handle_application_command(mock_interaction, {}, mock_client)

    mock_func.assert_called_once()
