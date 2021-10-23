import pytest
import nest_asyncio  # type: ignore
from unittest.mock import AsyncMock, patch

from src.dyscord.objects import Message

from . import samples
from ..guild import samples as guild_samples
from ..channel import samples as channel_samples


@pytest.mark.asyncio
@patch('src.dyscord.client.api.API')
async def test_text_interaction(api_mock):
    api_mock.get_guild = AsyncMock(return_value=guild_samples.discord_dev_example)
    api_mock.get_channel = AsyncMock(return_value=channel_samples.dev_guild_text)
    nest_asyncio.apply()

    obj = Message().from_dict(samples.short_message)
    obj.guild
    obj.channel

    api_mock.get_guild.assert_called()
    api_mock.get_channel.assert_called()
