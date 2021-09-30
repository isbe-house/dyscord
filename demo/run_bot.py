# flake8: noqa

# Handle the weirdness of our docker env first
from pprint import pprint
import sys
sys.path.insert(0, '.')

# Do normal imports and run!
import logging
import uuid

from src.simple_discord.utilities import Log
from src.simple_discord.client import DiscordClient, API
from src.simple_discord import objects, utilities
from src.simple_discord.objects.interactions import Command
from demo.everters import on_interaction

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

async def purge_commands(client, message):
    client._log.info('Get global commands')
    commands = await API.get_global_application_commands()
    for command in commands:
        command = Command().from_dict(command)
        assert command.id is not None
        await API.delete_global_application_command(command.id)

    client._log.info('Get guild commands')
    for guild in utilities.Cache().guilds:
        commands = await API.get_guild_application_commands(guild.id)
        for command in commands:
            command = Command().from_dict(command)
            assert command.id is not None
            await API.delete_guild_application_command(guild.id, command.id)

async def register_commands(client):
    new_command = Command()
    new_command.generate(
        name='chat',
        description='This is a more complex test.',
        type=objects.interactions.enumerations.COMMAND_TYPE.CHAT_INPUT,
    )
    new_command.add_option_typed(
        type=objects.interactions.enumerations.COMMAND_OPTION.BOOLEAN,
        name='hit_them',
        description='Age of the target',
    )
    new_command.validate()
    data1 = new_command.to_dict()

    new_command = Command()
    new_command.generate(
        name='user',
        description='',
        type=objects.interactions.enumerations.COMMAND_TYPE.USER,
    )
    new_command.validate()
    data2 = new_command.to_dict()

    new_command = Command()
    new_command.generate(
        name='message',
        description='',
        type=objects.interactions.enumerations.COMMAND_TYPE.MESSAGE,
    )
    new_command.validate()
    data3 = new_command.to_dict()

    registration = await API.create_global_application_command(data1)
    log.info(f'Registration1: {registration}')
    registration = await API.create_global_application_command(data2)
    log.info(f'Registration2: {registration}')
    registration = await API.create_global_application_command(data3)
    log.info(f'Registration3: {registration}')


async def list_commands(client):
    client._log.info('Get global commands')
    commands = await API.get_global_application_commands()
    for command in commands:
        command = Command().from_dict(command)
        log.info(command)

    client._log.info('Get guild commands')
    for guild in utilities.Cache().guilds:
        log.info(guild)
        commands = await API.get_guild_application_commands(guild.id)
        for command in commands:
            command = Command().from_dict(command)
            log.info(command)


async def send_buttons(client, chan_id):
    msg = objects.Message()
    channel = objects.TextChannel()
    channel.id = chan_id

    msg.content = 'Hello World!'

    row = msg.add_components()
    row.add_button(objects.interactions.enumerations.BUTTON_STYLES.DANGER, label='DO NOT PRESS', custom_id = str(uuid.uuid4()))

    await channel.send_message(msg)


@client.register_handler('MESSAGE_CREATE')
async def parse_message(client, message: objects.Message, raw_message):
    if client.me in message.mentions:
        log.info(f'Saw message: {message.content} from {message.author}')
        if 'PURGE' in message.content:
            log.critical('Purging all commands.')
            await purge_commands(client, message)

            assert type(message.channel) is objects.TextChannel
            await message.channel.send_message('Purged commands!')
        elif 'REGISTER' in message.content:
            log.critical('Registering test commands.')
            await register_commands(client)
        elif 'BUTTON' in message.content:
            log.critical('Create and send some components.')
            await send_buttons(client, message.channel_id)
        elif 'LIST' in message.content:
            log.critical('List components.')
            await list_commands(client)

client.run()
