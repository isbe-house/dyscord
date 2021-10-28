import logging
import pytest
import json
from importlib import reload

from src.dyscord.client import discord_client
from src.dyscord.client import enumerations

from tests.fixtures.fixtures import mock_api, mock_websocket  # noqa

# from ..objects.ready import samples as ready_samples


def test_basics():

    token = 'TOKEN STRING'

    application_id = 'APPLICATION ID'

    x = discord_client.DiscordClient(token, application_id)

    assert isinstance(x, discord_client.DiscordClient)


def test_intents():

    x = discord_client.DiscordClient('1234', '1234')

    x.set_all_intents()

    for intent in enumerations.INTENTS:
        assert x.intent & intent

    x.configure_intents(True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)

    for intent in enumerations.INTENTS:
        assert x.intent & intent


def test_reloading():

    reload(discord_client)
    assert not hasattr(discord_client.DiscordClient, 'token')

    x = discord_client.DiscordClient('foo')
    assert hasattr(discord_client.DiscordClient, 'token')
    assert hasattr(x, 'token')

    reload(discord_client)
    assert not hasattr(discord_client.DiscordClient, 'token')


@pytest.mark.asyncio
async def test_bad_event(caplog):

    caplog.set_level(logging.DEBUG)

    x = discord_client.DiscordClient('foo')
    discord_client.DiscordClient.ready = True

    await x._event_dispatcher({'d': None, 't': 'ILLEGAL TYPE'})

    print(caplog.text)

    assert 'ILLEGAL TYPE' in caplog.text
    assert 'Encountered unknown event' in caplog.text


@pytest.mark.asyncio
async def test_new_fixture(mock_websocket, mock_api):  # noqa

    mock_websocket.connect.return_value.__aenter__.return_value.recv.side_effect = [json.dumps({'t': None, 's': None, 'op': 10, 'd': {'heartbeat_interval': 41250}}), RuntimeError]

    x = discord_client.DiscordClient('1234', '5678')
    try:
        await x._web_socket_listener('foo')
    except RuntimeError:
        pass
