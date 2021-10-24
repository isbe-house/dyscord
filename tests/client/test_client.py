import logging
import pytest

from src.dyscord.client import DiscordClient
from src.dyscord.client import enumerations

# from ..objects.ready import samples as ready_samples


def test_basics():

    token = 'TOKEN STRING'

    application_id = 'APPLICATION ID'

    x = DiscordClient(token, application_id)

    assert isinstance(x, DiscordClient)


def test_intents():

    x = DiscordClient('1234', '1234')

    x.set_all_intents()

    for intent in enumerations.INTENTS:
        assert x.intent & intent

    x.configure_intents(True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)

    for intent in enumerations.INTENTS:
        assert x.intent & intent


def test_new_class():

    x = DiscordClient('foo')

    assert hasattr(DiscordClient, 'token')
    assert hasattr(x, 'token')


@pytest.mark.asyncio
async def test_bad_event(caplog):

    caplog.set_level(logging.DEBUG)

    x = DiscordClient('foo')
    DiscordClient.ready = True

    await x._event_dispatcher({'d': None, 't': 'ILLEGAL TYPE'})

    print(caplog.text)

    assert 'ILLEGAL TYPE' in caplog.text
    assert 'Encountered unknown event' in caplog.text
