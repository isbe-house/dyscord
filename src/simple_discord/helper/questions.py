import asyncio
from datetime import datetime, timedelta
from copy import copy
from typing import List

from ..objects.interactions import interaction as ext_interaction
from ..utilities import Log


class Question:
    _log = Log()
    '''Ask a user a question, respond with the answer.'''

    def __init__(self,
                 target: 'ext_interaction.InteractionStructure',
                 question: str,
                 answers: List['str'],
                 timeout: timedelta = timedelta(minutes=15),
                 cleanup: bool = False,
                 ):
        '''Build a question.

        Arguments:
            question (str): Question to ask the user.
            answers (List[str]): Responses the user can give.
        '''
        self.target = target
        self.question = question
        self.answers = copy(answers)
        self.timeout = timeout
        self.answer = None
        self.cleanup = cleanup
        self.last_interaction: 'ext_interaction.InteractionStructure'
        self._id_answer_map: dict = dict()

        assert len(self.answers) <= 25
        assert type(self.answers) in [list, tuple]

    async def ask(self) -> str:
        '''Ask a question.

        Arguments:
            target: Channel to target, or interaction to respond to.
        '''
        base = self.target.generate_response(type=self.target.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE)
        base.generate(content=self.question)
        ar = base.add_components()

        for answer in self.answers:
            if hasattr(ar, 'components') and (len(ar.components) == 5):
                ar = base.add_components()
            button = ar.add_button(ar.BUTTON_STYLES.PRIMARY, label=answer, callback=self._call_back)
            self._id_answer_map[button.custom_id] = answer

        await base.send()  # type: ignore

        start_datetime = datetime.now()

        while datetime.now() < start_datetime + self.timeout:
            await asyncio.sleep(1)
            if self.answer is not None:
                break

        return str(self.answer)

    async def _call_back(self, client, interaction: 'ext_interaction.InteractionStructure'):
        self.last_interaction = interaction
        if self.cleanup:
            print('RUN CLEANUP')
            response = self.target.generate_followup()
            await response.delete_initial_response()
        response = interaction.generate_response(type=interaction.INTERACTION_RESPONSE_TYPES.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE)
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
