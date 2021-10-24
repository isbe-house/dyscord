from src.dyscord.helper.interactions import Question, Confirmation
from src.dyscord.objects.interactions.interaction import Interaction
from src.dyscord.utilities.log import Log


async def test(interaction: Interaction):
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


async def complex(interaction: Interaction, client):
    raise RuntimeError
