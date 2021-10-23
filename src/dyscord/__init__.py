'''Dyscord is a library to enable a reasonably 1:1 binding between python and the official API.'''

from . import client, helper, objects, utilities
from .version import __version__
from .client.discord_client import DiscordClient

__all__ = [
    '__version__',
    'client',
    'DiscordClient',
    'helper',
    'objects',
    'utilities',
]
