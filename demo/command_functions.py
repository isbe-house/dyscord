import asyncio
from src.simple_discord.helper.questions import Question
from src.simple_discord.objects.interactions.interaction import InteractionStructure
from src.simple_discord.utilities.log import Log


async def test(client, interaction: InteractionStructure):

    try:
        assert interaction.data is not None
        cleanup: bool = interaction.data.options['cleanup'].value
    except Exception:
        cleanup: bool = True
    print(f'Test function got cleanup of [{cleanup}]')

    q = Question(interaction, 'What is your favorite bird?', ['Robin', 'Eagle', 'Crow'], cleanup=cleanup)
    answer = await q.ask()
    print(f'Got an answer of {answer}')

    await asyncio.sleep(5)

    followup = q.last_interaction.generate_followup()
    followup.generate(f'Thanks for the answer of {answer}!')
    await followup.send_followup_message()


async def complex(client, interaction: InteractionStructure):
    log = Log()
    from pprint import pformat

    assert interaction.data is not None

    if 'user' in interaction.data.options:
        log.info(f'Got [{interaction.data.options["user"]}]')
    if 'channel' in interaction.data.options:
        log.info(f'Got [{interaction.data.options["channel"]}]')

    response = interaction.generate_response(False, interaction.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE)
    response.generate(pformat(interaction.data.options))
    await response.send()
