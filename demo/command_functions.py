from src.simple_discord.helper.questions import Question, Confirmation
from src.simple_discord.objects.interactions.interaction import InteractionStructure
from src.simple_discord.utilities.log import Log


async def test(client, interaction: InteractionStructure):
    log = Log()

    try:
        log.info(f'[{interaction.data.options}]')
        assert interaction.data is not None
        cleanup: bool = interaction.data.options['cleanup']
    except Exception:
        log.critical('No cleanup give, assume true.')
        cleanup: bool = True

    cleanup = False
    auto_respond = True
    print(f'Test function got cleanup of [{cleanup}].')

    q = Question(interaction, 'What is your favorite bird?', ['Robin', 'Eagle', 'Crow'], cleanup=cleanup, auto_respond=auto_respond)
    await q.ask()

    a = await Confirmation(q, 'Are you sure?', auto_respond=True).ask()
    print(a)


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


async def hunt(client, interaction: InteractionStructure):

    assert interaction.data is not None

    from pprint import pprint

    pprint(interaction.data.options['stats']['game'].options)

    # re = interaction.generate_response(type=interaction.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE)
    # re.generate('Hello!')
    # await re.send()

    fu = interaction.generate_followup()
    fu.generate('Hello!')
    await fu.send()

    # confirm = Confirmation(interaction, 'Are you sure?')
    # con_answer = await confirm.ask()
    # print(f'Got [{con_answer}] which was of type [{type(con_answer)}]')

    # follow_up = confirm.last_interaction.generate_followup()
    # # await follow_up.delete_initial_response()

    # if con_answer is False or con_answer is None:
    #     # await follow_up.delete_initial_response()
    #     follow_up.generate('Okay, never mind then')
    #     await follow_up.send_followup_message()
    #     return

    # follow_up.generate('Saved the game!')
    # await follow_up.send_followup_message()
