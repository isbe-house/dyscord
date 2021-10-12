import datetime
import asyncio
from typing import List

from src.simple_discord.helper import CommandHandler
from src.simple_discord.objects import Snowflake, Message, TextChannel, interactions


class Question:

    def __init__(self,
                 channel_id: 'Snowflake',
                 timeout: datetime.timedelta = datetime.timedelta(minutes=15),
                 ):
        self.answered = False
        self.timeout = timeout
        self.target_channel_id = channel_id
        self._custom_ids: List[str] = list()

    async def handle_question(self) -> 'Question':
        '''Loop trough and wait for various questions to be answered. If timeout is reached, return.'''

        start_datetime = datetime.datetime.now()

        asyncio.create_task(self.question_1())

        while datetime.datetime.now() < start_datetime + self.timeout:
            await asyncio.sleep(1)
            if self.answered is True:
                break

        for custom_id in self._custom_ids:
            CommandHandler.unregister_interaction_custom_id(custom_id)

        return self

    async def question_1(self):
        '''Ask a question.'''
        # Register the question

        msg = Message()
        ar = msg.add_components()
        yes_button = ar.add_button(ar.BUTTON_STYLES.PRIMARY, label='YES')
        no_button = ar.add_button(ar.BUTTON_STYLES.PRIMARY, label='NO')
        msg.content = 'Do you want death or cake?'
        msg.validate()
        ch = TextChannel()
        ch.id = self.target_channel_id

        next_callback = self.answer_1

        CommandHandler.register_interaction_custom_id(yes_button.custom_id, next_callback, unlimited=True)
        CommandHandler.register_interaction_custom_id(no_button.custom_id, next_callback, unlimited=True)

        self._custom_ids.append(yes_button.custom_id)
        self._custom_ids.append(no_button.custom_id)

        msg: Message = await ch.send_message(msg)

    async def answer_1(self, client, interaction: 'interactions.InteractionStructure'):
        '''Handle answer.'''
        print('WE GOT IT!')

        response = interaction.generate_response(
            type=interaction.INTERACTION_RESPONSE_TYPES.UPDATE_MESSAGE,
            ephemeral=True,
        )
        response.data.generate(content='Thank you for your answers.')
        ar = response.data.add_components()
        ar.add_button(ar.BUTTON_STYLES.PRIMARY, label='YES')
        ar.add_button(ar.BUTTON_STYLES.PRIMARY, label='NO')

        await response.send()

        self.answered = True
