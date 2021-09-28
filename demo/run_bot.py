# flake8: noqa

# Handle the weirdness of our docker env first
import sys
sys.path.insert(0, '.')

# Do normal imports and run!
import logging

from src.simple_discord.utilities import Log
from src.simple_discord.client import DiscordClient, API
from src.simple_discord import objects, utilities

log = Log()
log.setLevel(logging.INFO)

log.info('Test')

try:
    with open('/run/secrets/discord_client_token') as fp:
        token = fp.read()
except FileNotFoundError:
    print('We did not find a \'discord_client_token\' file. Please create one!')
    raise
try:
    with open('/run/secrets/discord_application_id') as fp:
        application_id = fp.read()
except FileNotFoundError:
    print('We did not find a \'discord_application_id\' file. Please create one!')
    raise

client = DiscordClient(token=token, application_id=application_id)

client.configure_intents(
    guilds=True,
    guild_members=True,
    guild_messages=True,
    guild_message_reactions=True,
    guild_message_typeing=True,
    direct_messages=True,
)

@client.register_handler('READY')
async def on_ready(client, ready, raw_ready):
    log.critical('IT WORKS!')
    print(client)
    print(ready)
    print(raw_ready)

async def purge_commands(client):
    from pprint import pprint
    client._log.info('Get global commands')
    commands = await API.get_global_application_commands()
    for command in commands:
        command = objects.interactions.Command().from_dict(command)
        pprint(commands)
        assert command.id is not None
        await API.delete_global_application_command(command.id)

    client._log.info('Get guild commands')
    for guild in utilities.Cache().guilds:
        pprint(guild)
        commands = await API.get_guild_application_commands(guild.id)
        for command in commands:
            command = objects.interactions.Command().from_dict(command)
            pprint(command)
            assert command.id is not None
            await API.delete_guild_application_command(guild.id, command.id)

async def register_commands(client):
    new_command = objects.interactions.Command()
    new_command.generate(
        name='test2',
        description='This is a more complex test.',
        type=objects.interactions.enumerations.COMMAND_TYPE.CHAT_INPUT,
    )
    new_command.add_option_typed(
        type=objects.interactions.enumerations.COMMAND_OPTION.BOOLEAN,
        name='hit_them',
        description='Age of the target',
    )
    new_command.validate()
    data = new_command.to_dict()

    await API.create_global_application_command(data)


@client.register_handler('MESSAGE_CREATE')
async def parse_message(client, message, raw_message):
    if client.me in message.mentions:
        log.info(f'Saw message: {message.content}')
        if 'PURGE' in message.content:
            log.critical('Purging all commands.')
            await purge_commands(client)
        elif 'REGISTER' in message.content:
            log.critical('Registering test commands.')
            await register_commands(client)

client.run()
