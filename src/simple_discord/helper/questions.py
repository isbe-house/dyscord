import asyncio
from datetime import datetime, timedelta
from copy import copy
from typing import List, Union

from ..objects import channel, message
from ..objects.interactions import interaction
from ..utilities import Log


class Question:
    _log = Log()
    '''Ask a user a question, respond with the answer.'''

    def __init__(self, question: str, answers: List['str'], timeout: timedelta = timedelta(minutes=15)):
        '''Build a question.

        Arguments:
            question (str): Question to ask the user.
            answers (List[str]): Responses the user can give.
        '''
        self.question = question
        self.answers = copy(answers)
        self.timeout = timeout
        self.answer = None
        self.last_interaction: 'interaction.InteractionStructure'
        self._id_answer_map: dict = dict()

        assert len(self.answers) <= 25
        assert type(self.answers) in [list, tuple]

    async def ask(self,
                  target: Union['channel.Channel', 'interaction.InteractionStructure']
                  ) -> str:
        '''Ask a question.

        Arguments:
            target: Channel to target, or interaction to respond to.
        '''
        base: Union['message.Message', 'interaction.InteractionResponse'] = message.Message()
        if type(target) in [channel.TextChannel, channel.DMChannel]:
            base = message.Message(self.question)
        elif type(target) is interaction.InteractionStructure:
            base = target.generate_response(type=target.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE)
        assert base is not None
        ar = base.add_components()

        for answer in self.answers:
            if len(ar.components) == 5:
                ar = base.add_components()
            button = ar.add_button(ar.BUTTON_STYLES.PRIMARY, label=answer, callback=self._call_back)
            self._id_answer_map[button.custom_id] = answer

        if type(target) in [channel.TextChannel, channel.DMChannel]:
            await target.send_message(base)  # type: ignore
        elif type(target) is interaction.InteractionStructure:
            await base.send()  # type: ignore

        start_datetime = datetime.now()

        while datetime.now() < start_datetime + self.timeout:
            await asyncio.sleep(1)
            if self.answer is not None:
                break

        return str(self.answer)

    async def _call_back(self, client, interaction: 'interaction.InteractionStructure'):
        self.last_interaction = interaction
        response = interaction.generate_response(type=interaction.INTERACTION_RESPONSE_TYPES.DEFERRED_UPDATE_MESSAGE)
        await response.send()
        assert interaction.data is not None
        self.answer = self._id_answer_map[interaction.data.custom_id]

    # async def edit_initial_response(self):
    #     pass

    # async def delete_initial_response(self):
    #     pass

    # async def send_followup_message(self):
    #     pass

    # async def edit_original_message(self):
    #     pass


class CAPTCHA:
    '''Try to test humans from bots.'''
