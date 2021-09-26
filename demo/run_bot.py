# flake8: noqa

# Handle the weirdness of our docker env first
import sys
sys.path.insert(0, '.')

# Do normal imports and run!
import logging

from src.simple_discord.utilities import Log
from src.simple_discord.client import DiscordClient

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

client.run()
