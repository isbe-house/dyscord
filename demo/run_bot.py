# flake8: noqa

# Handle the weirdness of our docker env first
import sys

from src.simple_discord.objects.snowflake import Snowflake

sys.path.insert(0, '/usr/src/app/')

# Do normal imports and run!
import logging
import uuid

from src.simple_discord import objects, utilities
from src.simple_discord.client import DiscordClient, API
from src.simple_discord.objects.interactions import Command
from src.simple_discord.objects.message import Message
from src.simple_discord.utilities import Log
from src.simple_discord.objects.guild import Guild

from src import simple_discord
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

async def purge_commands(client, message: Message):
    client._log.info('Get global commands')
    commands = await API.get_global_application_commands()
    for command in commands:
        print(command)
        command = Command().from_dict(command)
        assert command.id is not None
        await API.delete_global_application_command(command.id)

    client._log.info('Get guild commands')
    assert message.guild is not None
    guild: Guild = message.guild
    commands = await API.get_guild_application_commands(guild.id)
    for command in commands:
        print(command)
        # command = Command().from_dict(command)
        # assert command.id is not None
        # await API.delete_guild_application_command(guild.id, command.id)


async def register_commands(client: simple_discord.client.DiscordClient, message):
    # Complex chat command

    guild = objects.Guild()
    guild.id = message.guild_id

    new_command = Command()
    new_command.generate(
        name='test',
        description='Generic test slash command.',
        type=objects.interactions.enumerations.COMMAND_TYPE.CHAT_INPUT,
    )
    new_command.add_option_typed(new_command.COMMAND_OPTION.BOOLEAN, 'cleanup', 'Cleanup commands after execution?', required=False)

    new_command.validate()

    registration = await new_command.register_to_guild(guild)
    log.info(f'Registration: {registration}')

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

    new_command.validate()

    registration = await new_command.register_to_guild(guild)
    log.info(f'Registration: {registration}')

    new_command = Command()
    new_command.generate(
        'hunt',
        'Hunt Showdown.',
        new_command.COMMAND_TYPE.CHAT_INPUT,
    )

    scg = new_command.add_option_sub_command_group(
        'stats',
        'Statistics about hunt.',
    )
    sc = scg.add_option_sub_command(
        'game',
        'Stats from a game',
    )

    sc.add_option_typed(sc.COMMAND_OPTION.INTEGER, 'p1-stars', 'Stars from player 1', required=True)
    sc.add_option_typed(sc.COMMAND_OPTION.INTEGER, 'p2-stars', 'Stars from player 1', required=False)
    sc.add_option_typed(sc.COMMAND_OPTION.INTEGER, 'p3-stars', 'Stars from player 1', required=False)

    sc.add_option_typed(sc.COMMAND_OPTION.BOOLEAN, 'survived', 'Did you survive?', required=False)
    sc.add_option_typed(sc.COMMAND_OPTION.INTEGER, 'bounties', 'How many bounties did the team extract?', required=False)
    sc.add_option_typed(sc.COMMAND_OPTION.INTEGER, 'kills', 'How many kills by the team?', required=False)
    co = sc.add_option_typed(sc.COMMAND_OPTION.STRING, 'map', 'Which map?', required=False)
    co.add_choice('lawson-delta', 'Lawson Delta')
    co.add_choice('stillwater-bayouu', 'Stillwater Bayouu')
    co.add_choice('desalle', 'DeSalle')

    new_command.validate()
    registration = await new_command.register_to_guild(guild)


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

@client.register_handler('ANY')
async def handle_any(client: simple_discord.client.DiscordClient, object, raw_object):

    m_client = Mongo.client
    type = raw_object.get('t', 'NA')
    type = f'type_{type}'
    m_client.dev.raw_events.insert_one(raw_object)
    m_client.dev[type].insert_one(raw_object)


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

simple_discord.helper.CommandHandler.register_guild_callback('test', command_functions.test)
simple_discord.helper.CommandHandler.register_guild_callback('complex', command_functions.complex)
simple_discord.helper.CommandHandler.register_guild_callback('hunt', command_functions.hunt)

Mongo.connect()
client.run()
