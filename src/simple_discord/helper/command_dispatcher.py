from typing import Optional

from ..objects import interactions, snowflake
from ..client import api
from ..utilities import Log


class CommandHandler:
    _log = Log()

    registered_commands = dict()

    global_lookup = dict()

    guild_lookup = dict()

    @classmethod
    async def command_handler(cls, client, interaction: 'interactions.InteractionStructure'):
        # Check to see if we have already registered this command
        if interaction.data is None:
            return

        # TODO: Support dispatching these too.
        if interaction.type != interactions.enumerations.INTERACTION_TYPES.APPLICATION_COMMAND:
            cls._log.info('Saw Application Command, we don\'t handled these yet!')
            return

        if interaction.data.id in cls.registered_commands:
            await cls.registered_commands[interaction.data.id](client, interaction)
            return

        if interaction.data.id not in cls.registered_commands:
            # Lookup command in global
            results = None
            try:
                results = await client.API.get_global_application_command(interaction.data.id)
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
                results = await client.API.get_guild_application_command(interaction.guild_id, interaction.data.id)
            except Exception:
                pass
            if (results is not None) and (results['name'] in cls.guild_lookup):
                cls.registered_commands[interaction.data.id] = cls.guild_lookup[results['name']]
            raise LookupError(f'Unable to find interaction {interaction.data.id} in Global or Guild!')

    @classmethod
    def register_global_callback(cls, command_name, callback_function, command_id: Optional['snowflake.Snowflake'] = None):
        cls.global_lookup[command_name] = callback_function
        if command_id is not None:
            cls.registered_commands[command_id] = callback_function

    @classmethod
    def register_guild_callback(cls, command_name, callback_function, command_id: Optional['snowflake.Snowflake'] = None):
        cls.guild_lookup[command_name] = callback_function
        if command_id is not None:
            cls.registered_commands[command_id] = callback_function
