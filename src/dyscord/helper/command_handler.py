import warnings
import inspect
import functools
import httpx
from cachetools import TTLCache
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional, Union, Any, Tuple

from ..objects import interactions, snowflake, guild as ext_guild
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

    registered_commands: 'Dict[snowflake.Snowflake, Callable]' = dict()

    global_lookup: 'Dict[str, Callable]' = dict()

    guild_lookup: 'Dict[Tuple[str, Optional[snowflake.Snowflake]], Callable]' = dict()

    registered_custom_ids: 'TTLCache[str, CallbackData]' = TTLCache(
        maxsize=float('inf'),
        ttl=timedelta(minutes=15),  # type: ignore
        timer=datetime.now,  # type: ignore
    )

    @classmethod
    def decorate_global_callback(cls):
        '''WIP Decorator to register against a target interaction.'''
        pass

    @classmethod
    def decorate_guild_callback(cls):
        '''WIP Decorator to register against a target interaction.'''
        pass

    @classmethod
    def register_global_callback(cls, command_name, callback_function, command_id: Optional['snowflake.Snowflake'] = None) -> None:
        '''Register name of a command to a given callback function globally.'''
        cls.global_lookup[command_name] = callback_function
        if command_id is not None:
            cls.registered_commands[command_id] = callback_function

    @classmethod
    def register_guild_callback(cls,
                                command_name: str,
                                callback_function: 'Callable',
                                guild: 'Optional[Union[snowflake.Snowflake, ext_guild.Guild]]' = None,
                                command_id: 'Optional[snowflake.Snowflake]' = None
                                ) -> None:
        '''Register name of a command to a given callback function for guilds.

        Arguments:
            command_name (str): Name of the command to be registered. MUST match the name registered with Discord!
            callback_function (Callable): Callback function. Must be a function which accepts either (Interaction) or (Interaction, DiscordClient) as arguments.
            guild (Snowflake|Guild): Target guild to trigger against. Leave empty if all guilds will use this same named command.
            command_id (Snowflake): If known, register the command_id now. Saves an API call later.
        '''
        if isinstance(guild, ext_guild.Guild):
            guild = guild.id

        cls.guild_lookup[(command_name, guild)] = callback_function
        if command_id is not None:
            cls.registered_commands[command_id] = callback_function

    @classmethod
    def register_interaction_custom_id(cls, custom_id: str, callback_function: Callable, unlimited: bool = False):
        '''Register a callback for an interaction.

        Arguments:
            custom_id (str): The custom id to trigger on.
            callback_function (Callable): Function to call when interaction is triggered.
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
        key: Tuple[Any, Optional['snowflake.Snowflake']]

        cls._log.info(f'Attempt lookup of [{interaction.data.name}] with id [{interaction.data.id}].')

        if interaction.data.id in cls.registered_commands:
            cls._log.info(f'Found [{interaction.data.id}] in registered commands.')
            await cls._determine_args_and_call(cls.registered_commands[interaction.data.id], client, interaction)
            return

        # Lookup command in global
        try:
            results = await api.API.get_global_application_command(interaction.data.id)
            cls._log.info('Attempt lookup inside global.')
            if results['name'] in cls.global_lookup:
                cls.registered_commands[interaction.data.id] = cls.global_lookup[results['name']]
                await cls._determine_args_and_call(cls.registered_commands[interaction.data.id], client, interaction)
                return
        except httpx.HTTPStatusError:
            pass

        # Lookup command in guild
        if (not hasattr(interaction, 'guild_id')) or (interaction.guild_id is None):
            return
        try:
            assert type(interaction.guild_id) is snowflake.Snowflake
            results = await api.API.get_guild_application_command(interaction.guild_id, interaction.data.id)

            key = (results['name'], interaction.guild_id)
            cls._log.info('Attempt lookup inside guild.')
            if (key in cls.guild_lookup):
                cls.registered_commands[interaction.data.id] = cls.guild_lookup[key]
                await cls._determine_args_and_call(cls.registered_commands[interaction.data.id], client, interaction)
                return

            key = (results['name'], None)
            cls._log.info('Attempt lookup inside ALL guilds.')
            if (key in cls.guild_lookup):
                cls.registered_commands[interaction.data.id] = cls.guild_lookup[key]
                await cls._determine_args_and_call(cls.registered_commands[interaction.data.id], client, interaction)
                return
        except httpx.HTTPStatusError:
            pass

        raise LookupError(f'Unable to find interaction [{interaction.data.id}] in Global or Guild!')

    @classmethod
    async def _determine_args_and_call(cls, callable, client, interaction: 'interactions.Interaction') -> None:
        assert interaction.data is not None
        arg_len = len(inspect.signature(callable).parameters)
        if cls.__iscoroutinefunction_or_partial(callable):
            if arg_len == 1:
                await cls.registered_commands[interaction.data.id](interaction)
            elif arg_len == 2:
                await cls.registered_commands[interaction.data.id](interaction, client)
        else:
            if arg_len == 1:
                cls.registered_commands[interaction.data.id](interaction)
            elif arg_len == 2:
                cls.registered_commands[interaction.data.id](interaction, client)
            warnings.warn('While sync functions are supported as callbacks in CommandHandler, they are STRONGLY counter-recommended!', UserWarning)

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
            callback_data.callback(client, interaction)
            warnings.warn('While sync functions are supported as callbacks in CommandHandler, they are STRONGLY counter-recommended!', UserWarning)

    @classmethod
    def __iscoroutinefunction_or_partial(cls, object):
        while isinstance(object, functools.partial):
            object = object.func
        return inspect.iscoroutinefunction(object)
