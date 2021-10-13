import asyncio
from src.simple_discord.helper.questions import Question
from src.simple_discord.objects.interactions import InteractionStructure
from src import simple_discord


async def global_complex(client, interaction: InteractionStructure):
    assert interaction.data is not None
    target_user = interaction.data.options[0].options[0].options[0].value
    response = interaction.generate_response(True, interaction.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE)
    user = simple_discord.objects.User()
    user.id = target_user
    response.data.generate(content=f'Should I slap {user.mention_nickname}?')
    ar = response.data.add_components()
    ar.add_button(ar.BUTTON_STYLES.SUCCESS,label='YES!', callback=yes)
    ar.add_button(ar.BUTTON_STYLES.DANGER,label='NO!', callback=no)
    await response.send()

async def yes(client, interaction: InteractionStructure):
    print('YES')
    response = interaction.generate_response(True, interaction.INTERACTION_RESPONSE_TYPES.UPDATE_MESSAGE)
    response.data.generate(content='Ok!')
    await response.send()

async def no(client, interaction: InteractionStructure):
    print('NO')
    response = interaction.generate_response(True, interaction.INTERACTION_RESPONSE_TYPES.UPDATE_MESSAGE)
    response.data.generate(content='Ok!')
    await response.send()

    await asyncio.sleep(5)

    follow_up = interaction.generate_followup()
    follow_up.generate(content='This is a follow up!')
    e = follow_up.add_embeds()
    e.generate('Embed Title')
    e.add_field('Scouts', f'{1234:,d}')
    await follow_up.send_send_followup_message()

    await follow_up.send_delete_initial_response()


simple_discord.helper.CommandHandler.register_global_callback('complex', global_complex)
simple_discord.helper.CommandHandler.register_guild_callback('complex', global_complex)
