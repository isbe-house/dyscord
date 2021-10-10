from typing import Optional
from src.simple_discord.client import DiscordClient
from src.simple_discord.objects import snowflake
from src.simple_discord.objects.interactions import InteractionStructure
from src.simple_discord.objects.interactions.enumerations import BUTTON_STYLES
from src import simple_discord


async def global_complex(client, interaction: InteractionStructure):
    assert interaction.data is not None
    target_user = interaction.data.options[0].options[0].options[0].value
    response = interaction.generate_response(True, interaction.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE)
    user = simple_discord.objects.User()
    user.id = target_user
    response.data.generate(content=f'I\'m gonna slap {user.mention_nickname}!')
    await response.send()


simple_discord.helper.CommandHandler.register_global_callback('complex', global_complex)
