import asyncio
from abc import ABC
from datetime import datetime, timedelta
from copy import copy
from typing import Any, List, Union, Optional

from ..objects.interactions import interaction as ext_interaction
from ..utilities import Log


class InteractionResponseHelper(ABC):
    '''Assistive classes to help with responding to an interaction.'''

    _log = Log()

    def __init__(self,
                 target: Union['ext_interaction.Interaction', 'InteractionResponseHelper'],
                 question: str,
                 timeout: timedelta = timedelta(minutes=15),
                 cleanup: bool = False,
                 auto_respond: bool = False,
                 ):
        '''Constructor for abstract Interaction Response Helpers.'''
        self.target = target
        self.question = question
        self.timeout = timeout
        self.cleanup = cleanup
        self.last_interaction: 'ext_interaction.Interaction'
        self.answer: Any = None
        self.auto_respond: bool = auto_respond

        if self.cleanup and self.auto_respond:
            raise ValueError('You cannot set cleanup and auto_respond to \'True\' at the same time.')

        self._id_answer_map: dict = dict()
        self._answered: bool = False
        self._initial_was_response: Optional[bool] = None

    def _ask_base_generation(self) -> Union['ext_interaction.InteractionResponse', 'ext_interaction.InteractionFollowup']:
        '''From the target, generate a base which is appropriate for the interaction.'''
        if isinstance(self.target, InteractionResponseHelper):
            if not self.target._answered:
                raise RuntimeError('Unanswered questions don\'t have interactions yet. You must ask the previous question first.')
            target = self.target.last_interaction
        else:
            target = self.target

        base: Union[ext_interaction.InteractionFollowup, ext_interaction.InteractionResponse]
        if target.can_respond:
            base = target.generate_response(type=target.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE, ephemeral=True)
            self._initial_was_response = True
        else:
            base = target.generate_followup(ephemeral=True)
            self._initial_was_response = False
        return base

    async def _wait_for_answer(self):
        start_datetime = datetime.now()

        while datetime.now() < start_datetime + self.timeout:
            await asyncio.sleep(1)
            if self._answered is True:
                break

    async def _call_back(self, client, interaction: 'ext_interaction.Interaction'):
        self._answered = True
        self.last_interaction = interaction
        assert interaction.data is not None
        self.answer = self._id_answer_map[interaction.data.custom_id]
        if self.cleanup:
            response = self.target.generate_followup()
            await response.delete_initial_response()
        if self.auto_respond:
            response = interaction.generate_response(type=interaction.INTERACTION_RESPONSE_TYPES.UPDATE_MESSAGE)
            response.generate(content=f'Question: `{self.question}`, You answered: `{self.answer}`')
            await response.send()

    def generate_response(self, type: 'ext_interaction.enumerations.INTERACTION_RESPONSE_TYPES' = None, ephemeral: bool = True):
        '''Generate a response from the interaction.

        Raises:
            RuntimeError: When cleanup or auto_respond are set to true.
        '''
        if self.cleanup:
            raise RuntimeError('You cannot respond to a message you asked us to cleanup.')
        if self.auto_respond:
            raise RuntimeError('You cannot respond to a message you asked us to auto-respond to.')
        if type is None:
            type = ext_interaction.enumerations.INTERACTION_RESPONSE_TYPES.UPDATE_MESSAGE
        return self.last_interaction.generate_response(type, ephemeral)

    def generate_followup(self, ephemeral: bool = True):
        '''Generate a followup to the interaction.'''
        if self.cleanup:
            raise RuntimeError('You cannot respond to a message you asked us to cleanup.')
        return self.last_interaction.generate_followup(ephemeral)


class Question(InteractionResponseHelper):
    '''Ask a user a question, respond with the answer.'''

    _log = Log()

    def __init__(self,
                 target: Union['ext_interaction.Interaction', 'InteractionResponseHelper'],
                 question: str,
                 answers: List['str'],
                 timeout: timedelta = timedelta(minutes=15),
                 cleanup: bool = False,
                 auto_respond: bool = False,
                 ):
        '''Prompt user with a question to be answered by one of a list of specific answers.

        Arguments:
            target (Interaction|InteractionResponseHelper): Object to be responded to. Commonly an interaction, but you can chain InteractionResponseHelpers together.
            question (str): Actual text of the question to prompt the user with.
            answers (str): List of valid answers the user can give.
            timeout (timedelta): Time before the response helper gives up.
            cleanup (bool): Should we delete this when an answer is received? Mutually exclusive with `auto_response`.
            auto_respond (bool): Should we give feedback to the user when an answer is received? Mutually exclusive with `clean_up`.
        '''
        super().__init__(target, question, timeout, cleanup, auto_respond)
        self.answers = copy(answers)

        assert len(self.answers) <= 25
        assert type(self.answers) in [list, tuple]

    async def ask(self) -> str:
        '''Ask a question.

        Returns:
            bool: Result from user. Will be `None` if user selected Cancel, or a timeout occurs.
        '''
        assert type(self.target) is ext_interaction.Interaction
        base = self.target.generate_response(type=self.target.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE)
        base.generate(content=self.question)
        ar = base.add_components()

        for answer in self.answers:
            if hasattr(ar, 'components') and (len(ar.components) == 5):
                ar = base.add_components()
            button = ar.add_button(ar.BUTTON_STYLES.PRIMARY, label=answer, callback=self._call_back)
            self._id_answer_map[button.custom_id] = answer

        await base.send()  # type: ignore
        await self._wait_for_answer()
        return str(self.answer)


class CAPTCHA:
    '''Try to test humans from bots.'''


class Confirmation(InteractionResponseHelper):
    '''Ask a user for a YES/NO/CANCEL response.'''

    _log = Log()

    def __init__(self,
                 target: Union['ext_interaction.Interaction', 'InteractionResponseHelper'],
                 question: str,
                 timeout: timedelta = timedelta(minutes=15),
                 cleanup: bool = False,
                 auto_respond: bool = False,
                 ):
        '''Ask the user to confirm, deny, or cancel.

        Arguments:
            target (Interaction, InteractionResponseHelper): Target of this interaction.
            question (str): Actual text of the question to prompt the user with.
            timeout (timedelta): Time before the response helper gives up.
            cleanup (bool): Should we delete this when an answer is received? Mutually exclusive with `auto_response`.
            auto_respond (bool): Should we give feedback to the user when an answer is received? Mutually exclusive with `clean_up`.
        '''
        super().__init__(target, question, timeout, cleanup, auto_respond)

    async def ask(self) -> bool:
        '''Ask a question.

        Returns:
            bool: Result from user. Will be `None` if user selected Cancel, or a timeout occurs.
        '''
        base = self._ask_base_generation()
        base.generate(content=self.question)
        ar = base.add_components()

        button = ar.add_button(ar.BUTTON_STYLES.SUCCESS, label='Yes', callback=self._call_back)
        self._id_answer_map[button.custom_id] = True

        button = ar.add_button(ar.BUTTON_STYLES.DANGER, label='No', callback=self._call_back)
        self._id_answer_map[button.custom_id] = False

        button = ar.add_button(ar.BUTTON_STYLES.SECONDARY, label='Cancel', callback=self._call_back)
        self._id_answer_map[button.custom_id] = None

        await base.send()
        await self._wait_for_answer()
        return self.answer
