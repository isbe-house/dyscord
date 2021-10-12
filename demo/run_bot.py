# flake8: noqa

# Handle the weirdness of our docker env first
import sys

sys.path.insert(0, '.')

# Do normal imports and run!
import logging
import uuid
from datetime import datetime, timedelta

from src.simple_discord.utilities import Log
from src.simple_discord.client import DiscordClient, API
from src.simple_discord import objects, utilities
from src.simple_discord.objects.interactions import Command
from src import simple_discord
from demo import everters
from demo.interaction import Question

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

@client.register_handler('READY')
def on_ready2(client, ready, raw_ready):
    log.critical('IT WORKS!')

@client.register_class
class Foo:

    async def on_ready(self, client, ready, raw_ready):
        log.critical('IT WORKS!')

    async def on_message_create(self, client, message, raw_message):
        log.info('Saw a message.')

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

async def fleet_handler(client, interaction: simple_discord.objects.interactions.InteractionStructure):
    pass

async def register_commands(client: simple_discord.client.DiscordClient, message):
    # Complex chat command

    new_command = Command()
    new_command.generate(
        name='complex',
        description='This is a more complex test.',
        type=objects.interactions.enumerations.COMMAND_TYPE.CHAT_INPUT,
    )
    scg = new_command.add_option_sub_command_group('edit', 'edit stuff')
    sc = scg.add_option_sub_command('user', 'Edit a user')
    sc.add_option_typed(sc.COMMAND_OPTION.USER, name='target', description='The poor sap you are gonna hit')

    new_command.validate()

    registration = await new_command.register_globally()
    log.info(f'Registration3: {registration}')

    new_command = Command()
    new_command.generate(
        name='fleet',
        description='This is a more complex test.',
        type=objects.interactions.enumerations.COMMAND_TYPE.CHAT_INPUT,
    )
    scg = new_command.add_option_sub_command_group('manage', 'edit stuff')
    sc = scg.add_option_sub_command('move_ships', 'Edit a user')
    sc.add_option_typed(
        sc.COMMAND_OPTION.INTEGER,
        name='source',
        description='.',
    )
    sc.add_option_typed(
        sc.COMMAND_OPTION.INTEGER,
        name='destination',
        description='.',
    )
    opt = sc.add_option_typed(
        sc.COMMAND_OPTION.STRING,
        name='ship_type',
        description='.',
    )
    opt.add_choice('frigate', 'frigate')
    opt.add_choice('scout', 'scout')
    sc.add_option_typed(
        sc.COMMAND_OPTION.INTEGER,
        name='ship_number',
        description='.',
    )

    sc = scg.add_option_sub_command('launch_fleet', 'Edit a user')
    sc.add_option_typed(
        sc.COMMAND_OPTION.STRING,
        name='target',
        description='.',
    )
    # scg = new_command.add_option_sub_command_group('spawn', 'edit stuff')
    sc = new_command.add_option_sub_command('create', 'Edit a user')
    sc.add_option_typed(
        sc.COMMAND_OPTION.STRING,
        name='name',
        description='.',
    )

    new_command.validate()

    guild = objects.Guild()
    guild.id = message.guild_id

    registration = await new_command.register_to_guild(guild)
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


async def test(client, message: objects.Message):

    new_msg = objects.Message()
    new_msg.content = f'The guild is {message.guild}'
    assert type(message.channel) is objects.TextChannel
    await message.channel.send_message(new_msg)

    q = Question(message.channel_id)
    await q.handle_question()
    log.info('Finished test!')


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

simple_discord.helper.CommandHandler.register_guild_callback('fleet', fleet_handler)

client.run()
