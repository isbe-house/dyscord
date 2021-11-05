import difflib

from src.dyscord.objects.interactions.interaction import Interaction
from src.dyscord.utilities.log import Log


async def test(interaction: Interaction):
    log = Log()
    if interaction.type == Interaction.INTERACTION_TYPES.APPLICATION_COMMAND_AUTOCOMPLETE:
        log.info('Process autocompete interactio.')
        print('Server asking for auto complete, lets give it to them!')
        response = interaction.generate_response(interaction.INTERACTION_RESPONSE_TYPES.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT)

        with open('demo/words.txt') as fp:
            demo_names = fp.read()

        demo_names = demo_names.split('\n')

        print(demo_names[:5])
        print(type(demo_names))

        assert interaction.data is not None
        choices = difflib.get_close_matches(interaction.data.options['name'].value, demo_names, 5, cutoff=0)

        while len(choices) < 5:
            choices.append(demo_names[0])

        for choice in choices:
            response.add_choice(choice, choice)

        print(response.to_dict())
        await response.send()
        return

    log.info('Process full interaction.')
    response = interaction.generate_response()
    response.generate('Okay!', ephemeral=True)
    await response.send()


async def complex(interaction: Interaction):
    response = interaction.generate_response(interaction.INTERACTION_RESPONSE_TYPES.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE, ephemeral=True)
    await response.send()
