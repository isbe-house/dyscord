'''Dyscord is a library to enable a reasonably 1:1 binding between python and the official API.'''

from . import client, helper, objects, utilities
from .version import __version__

__all__ = [
    'client',
    'helper',
    'objects',
    'utilities',
    '__version__',
]
