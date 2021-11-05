# flake8: noqa

# Handle the weirdness of our docker env first
import sys

sys.path.insert(0, '/usr/src/app/')

# Do normal imports and run!
import logging
import uuid

from src.dyscord import objects, utilities
from src.dyscord.client import DiscordClient, API
from src.dyscord.objects.interactions import Command
from src.dyscord.objects.message import Message
from src.dyscord.objects import Snowflake
from src.dyscord.utilities import Log
from src.dyscord.objects.guild import Guild

from src import dyscord
from demo import command_functions
from demo.mongo import Mongo

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

client.set_all_intents()

async def purge_commands(client, message: Message):
    client._log.info('Get global commands')
    commands = await API.get_global_application_commands()
    for command in commands:
        command = Command().from_dict(command)
        assert command.id is not None
        await API.delete_global_application_command(command.id)

    client._log.info('Get guild commands')
    assert message.guild is not None
    guild: Guild = message.guild
    commands = await API.get_guild_application_commands(guild.id)
    for command in commands:
        command = Command().from_dict(command)
        print(command.name)
        assert command.id is not None
        await API.delete_guild_application_command(guild.id, command.id)


async def register_commands(client: dyscord.client.DiscordClient, message):
    # Complex chat command

    guild = objects.Guild()
    guild.id = message.guild_id

    new_command = Command()
    new_command.generate(
        name='test',
        description='Generic test slash command.',
        type=objects.interactions.enumerations.COMMAND_TYPE.CHAT_INPUT,
    )
    new_command.add_option_typed(new_command.COMMAND_OPTION.STRING, 'name', 'Guess a name.', autocomplete=True)

    new_command.validate()

    registration = await new_command.register_to_guild(guild)
    log.info(f'Registration: {registration}')
    # registration = await new_command.register_globally()
    # log.info(f'Registration: {registration}')

    new_command = Command()
    new_command.generate(
        name='complex',
        description='Test lots of complicated things.',
        type=objects.interactions.enumerations.COMMAND_TYPE.CHAT_INPUT,
    )

    new_command.add_option_typed(new_command.COMMAND_OPTION.CHANNEL, 'channel', 'Channel test', required=False)
    new_command.add_option_typed(new_command.COMMAND_OPTION.USER, 'user', 'User test', required=False)
    new_command.add_option_typed(new_command.COMMAND_OPTION.INTEGER, 'int', 'A simple number', required=False)
    new_command.add_option_typed(new_command.COMMAND_OPTION.MENTIONABLE, 'mention', 'Mention someone', required=False)
    new_command.add_option_typed(new_command.COMMAND_OPTION.NUMBER, 'float', 'Float something BIG', required=False)
    new_command.add_option_typed(new_command.COMMAND_OPTION.STRING, 'string', 'String of something', required=False)
    new_command.add_option_typed(new_command.COMMAND_OPTION.BOOLEAN, 'bool', 'True or false', required=False)
    new_command.add_option_typed(new_command.COMMAND_OPTION.ROLE, 'role', 'Some Role.', required=False)
    new_command.add_option_typed(new_command.COMMAND_OPTION.MENTIONABLE, 'mentionable', 'Something you can mention Role.', required=False)

    new_command.validate()

    registration = await new_command.register_to_guild(guild)
    log.info(f'Registration: {registration}')
    # registration = await new_command.register_globally()
    # log.info(f'Registration: {registration}')


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


async def test(client, message: objects.Message):
    await API.get_user(Snowflake('185846097284038656'))


async def handle_any(data: dict):
    m_client = Mongo.client
    type = data.get('t', 'NA')
    type = f'type_{type}'
    m_client.dev.raw_events.insert_one(data)
    m_client.dev[type].insert_one(data)


@client.decorate_handler('MESSAGE_CREATE')
async def parse_message(message: objects.Message, raw_message, client):
    if client.me in message.mentions:
        log.info(f'Saw message: {message.content} from {message.author}')
        if 'PURGE' in message.content:
            log.critical('Purging all commands.')
            await purge_commands(client, message)
            assert type(message.channel) is objects.TextChannel
            await message.channel.send_message('Purged commands!')
        elif 'REGISTER' in message.content:
            log.critical('Registering test commands.')
            await register_commands(client, message)
        elif 'BUTTON' in message.content:
            log.critical('Create and send some components.')
            await send_buttons(client, message.channel_id)
        elif 'LIST' in message.content:
            log.critical('List components.')
            await list_commands(client)
        elif 'TEST' in message.content:
            log.critical('Run test command.')
            assert type(message) is objects.Message
            await test(client, message)

dyscord.helper.CommandHandler.register_guild_callback('test', command_functions.test)
dyscord.helper.CommandHandler.register_guild_callback('complex', command_functions.complex)
dyscord.helper.CommandHandler.register_global_callback('test', command_functions.test)
dyscord.helper.CommandHandler.register_global_callback('complex', command_functions.complex)

client._register_raw_callback(handle_any)

Mongo.connect()
client.run()
