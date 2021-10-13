from src.simple_discord.helper.questions import Question
from src.simple_discord.objects.interactions.interaction import InteractionStructure


async def test(client, interaction: InteractionStructure):
    q = Question('What is your favorite bird?', ['Robin', 'Eangle', 'Crow'])
    answer = await q.ask(interaction)
    print(f'Got an answer of {answer}')
