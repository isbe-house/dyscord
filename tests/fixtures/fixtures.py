import pytest
from unittest.mock import AsyncMock, patch

from . import samples


@pytest.fixture
def mock_websocket():
    with patch('src.dyscord.client.discord_client.websockets') as mock:
        yield mock


@pytest.fixture
def mock_api():
    with patch('src.dyscord.client.api.API') as mock:
        mock.get_user = AsyncMock(return_value=samples.dev_user)
        yield mock
