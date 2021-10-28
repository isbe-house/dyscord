import datetime

import pytest
from unittest.mock import AsyncMock, patch, Mock, sentinel

from . import samples

from ..objects.channel import samples as channel_samples
from ..objects.role import samples as role_samples


@pytest.fixture
def mock_websocket():
    with patch('src.dyscord.client.discord_client.websockets') as mock:
        yield mock


@pytest.fixture
def mock_api():
    with patch('src.dyscord.client.api.API', spec=True) as mock:
        mock.get_user = AsyncMock(return_value=samples.dev_user)
        mock.get_channel = AsyncMock(return_value=channel_samples.dev_guild_text)
        mock.get_guild_roles = AsyncMock(return_value=[role_samples.dev_role])
        yield mock


@pytest.fixture
def mock_httpx():
    with patch('httpx.AsyncClient.__aenter__', spec=True) as mock:
        mock.return_value.patch.return_value.raise_for_status = Mock()
        mock.return_value.patch.return_value.headers = dict(
            {
                'x-ratelimit-reset': datetime.datetime.now().timestamp(),
                'x-ratelimit-remaining': 1,
            }
        )
        mock.return_value.patch.return_value.json = Mock(return_value=sentinel.JSON_RETURN)
        mock.return_value.patch.return_value.raise_for_status = Mock()

        mock.return_value.delete.return_value.raise_for_status = Mock()
        mock.return_value.delete.return_value.headers = dict(
            {
                'x-ratelimit-reset': datetime.datetime.now().timestamp(),
                'x-ratelimit-remaining': 1,
            }
        )
        mock.return_value.delete.return_value.json = Mock(return_value=sentinel.JSON_RETURN)

        mock.return_value.post.return_value.raise_for_status = Mock()
        mock.return_value.post.return_value.headers = dict(
            {
                'x-ratelimit-reset': datetime.datetime.now().timestamp(),
                'x-ratelimit-remaining': 1,
            }
        )
        mock.return_value.post.return_value.json = Mock(return_value=sentinel.JSON_RETURN)

        mock.return_value.get.return_value.raise_for_status = Mock()
        mock.return_value.get.return_value.headers = dict(
            {
                'x-ratelimit-reset': datetime.datetime.now().timestamp(),
                'x-ratelimit-remaining': 1,
            }
        )
        mock.return_value.get.return_value.json = Mock(return_value=sentinel.JSON_RETURN)
        yield mock
