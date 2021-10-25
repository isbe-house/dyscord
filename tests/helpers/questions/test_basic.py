import pytest
from unittest.mock import AsyncMock, patch

from src.dyscord.helper import Confirmation
# from src.dyscord.helper import Question

from src.dyscord.objects.interactions import Interaction
# from src.dyscord.objects import User

from ...objects.interactions import samples as interaction_samples
from ...objects.user import samples as user_samples


@pytest.fixture
@patch('src.dyscord.client.api.API')
def an_interaction(api_mock):
    api_mock.get_user = AsyncMock(return_value=user_samples.raw_get_user_response)
    x = Interaction()
    x.from_dict(interaction_samples.trigger_chat)
    return x


@patch('src.dyscord.client.api.API')
def test_init(api_mock, an_interaction):
    api_mock.get_user = AsyncMock(return_value=user_samples.raw_get_user_response)
    x = Confirmation(an_interaction, 'Are you sure?')
    assert x is not None
