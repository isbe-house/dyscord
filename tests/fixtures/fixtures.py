import pytest
from unittest.mock import AsyncMock, patch

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

        mock.create_interaction_response = AsyncMock()
        yield mock
