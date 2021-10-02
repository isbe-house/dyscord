from src.simple_discord.client import DiscordClient
from src.simple_discord.objects.interactions import InteractionStructure
from src.simple_discord.objects.interactions.enumerations import BUTTON_STYLES


@DiscordClient.register_handler(event='INTERACTION_CREATE')
async def on_interaction(client, interaction: InteractionStructure, raw_interaction):
    from pprint import pprint
    pprint(raw_interaction)

    assert interaction.data is not None
    pprint(interaction.data.to_dict())

    response = interaction.generate_response(True)
    response.type = response.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE
    response.data.generate(content='This is a personal response.')
    row = response.data.add_components()
    row.add_button(BUTTON_STYLES.PRIMARY, '1', 'PRESS ME')
    await response.send()
