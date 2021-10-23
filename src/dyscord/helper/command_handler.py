import warnings
import inspect
import functools
from cachetools import TTLCache
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional

from ..objects import interactions, snowflake
from ..utilities import Log
from ..client import api


@dataclass
class CallbackData:
    '''Callback dataclass.'''
    custom_id: str
    callback: Callable
    unlimited: bool


class CommandHandler:
    '''Manage commands for the user.'''
    _log = Log()

    registered_commands: Dict['snowflake.Snowflake', Callable] = dict()

    global_lookup: Dict[str, Callable] = dict()

    guild_lookup: Dict[str, Callable] = dict()

    registered_custom_ids: 'TTLCache[str, CallbackData]' = TTLCache(
        maxsize=float('inf'),
        ttl=timedelta(minutes=15),  # type: ignore
        timer=datetime.now,  # type: ignore
    )

    @classmethod
    def register_global_callback(cls, command_name, callback_function, command_id: Optional['snowflake.Snowflake'] = None) -> None:
        '''Register name of a command to a given callback function globally.'''
        cls.global_lookup[command_name] = callback_function
        if command_id is not None:
            cls.registered_commands[command_id] = callback_function

    @classmethod
    def register_guild_callback(cls, command_name, callback_function, command_id: Optional['snowflake.Snowflake'] = None) -> None:
        '''Register name of a command to a given callback function for guilds.'''
        cls.guild_lookup[command_name] = callback_function
        if command_id is not None:
            cls.registered_commands[command_id] = callback_function

    @classmethod
    def register_interaction_custom_id(cls, custom_id: str, callback_function: Callable, unlimited: bool = False):
        '''Register a callback for an interaction.

        Arguments:
            custom_id (str): The custom id to trigger on.
            callback_function (Callable): Function to call when interaction is triggered. MUST be asnyc.
            unlimited (bool): Allows more than one interaction to be called. The user is expected to deregister this interaction later. If
                no cleanup occurs, the handler is cleaned after 15 minutes.
        '''
        # TODO: We can probably customize the duration of the cache at runtime?
        obj = CallbackData(custom_id, callback_function, unlimited)
        cls.registered_custom_ids[custom_id] = obj

    @classmethod
    def unregister_interaction_custom_id(cls, custom_id: str, not_exists_ok: bool = False):
        '''Attempt to remove a custom_id from the interaction cache. Warn if already removed.'''
        if custom_id in cls.registered_custom_ids:
            del cls.registered_custom_ids[custom_id]
        elif not not_exists_ok:
            cls._log.warning(f'Observed improper attempt to remove interaction_id [{custom_id}].')

    @classmethod
    async def command_handler(cls, client, interaction: 'interactions.Interaction') -> None:  # noqa: C901
        '''Handle incoming commands and dispatch them to the correct type handler.'''
        if interaction.data is None:
            return

        if interaction.type == interactions.enumerations.INTERACTION_TYPES.MESSAGE_COMPONENT:
            await cls.handle_message_component(client, interaction)
        elif interaction.type == interactions.enumerations.INTERACTION_TYPES.APPLICATION_COMMAND:
            await cls.handle_application_command(client, interaction)

    @classmethod
    async def handle_application_command(cls, client, interaction: 'interactions.Interaction') -> None:
        '''Handle interactions against Messages and Users.'''
        assert interaction.data is not None

        if interaction.data.id in cls.registered_commands:
            await cls.registered_commands[interaction.data.id](client, interaction)
            return

        if interaction.data.id not in cls.registered_commands:
            # Lookup command in global
            results = None
            try:
                results = await api.API.get_global_application_command(interaction.data.id)
            except Exception:
                pass
            if (results is not None) and (results['name'] in cls.global_lookup):
                cls.registered_commands[interaction.data.id] = cls.global_lookup[results['name']]
                await cls.registered_commands[interaction.data.id](client, interaction)
                return
            # Lookup command in guild
            if not hasattr(interaction, 'guild_id'):
                return
            try:
                assert type(interaction.guild_id) is snowflake.Snowflake
                results = await api.API.get_guild_application_command(interaction.guild_id, interaction.data.id)
            except Exception:
                pass
            if (results is not None) and (results['name'] in cls.guild_lookup):
                cls.registered_commands[interaction.data.id] = cls.guild_lookup[results['name']]
                await cls.registered_commands[interaction.data.id](client, interaction)
                return
            raise LookupError(f'Unable to find interaction {interaction.data.id} in Global or Guild!')

    @classmethod
    async def handle_message_component(cls, client, interaction: 'interactions.Interaction') -> None:
        '''Handle slash-commands.'''
        assert interaction.data is not None
        cls._log.info(f'Saw id [{interaction.id}] with custom id [{interaction.data.custom_id}].')
        assert interaction.data is not None
        if interaction.data.custom_id not in cls.registered_custom_ids:
            raise RuntimeError('Got unexpected interaction')

        callback_data = cls.registered_custom_ids[interaction.data.custom_id]
        if callback_data.unlimited is False:
            del cls.registered_custom_ids[interaction.data.custom_id]

        if cls.__iscoroutinefunction_or_partial(callback_data.callback):
            await callback_data.callback(client, interaction)
        else:
            warnings.warn('While sync functions are supported as callbacks in CommandHandler, they are STRONGLY counter-recommended!', UserWarning)
            callback_data.callback(client, interaction)

    @classmethod
    def __iscoroutinefunction_or_partial(cls, object):
        while isinstance(object, functools.partial):
            object = object.func
        return inspect.iscoroutinefunction(object)
