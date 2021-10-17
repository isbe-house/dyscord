'''Cache values for discord to use. NOT CURRENTLY USED.'''

from .. import objects
from .borg import Borg


class Cache(Borg):
    '''Generic cache of objects we have been told about from the API.'''

    def __init__(self):
        '''Create a access to the cache, follows the Borg design pattern.'''
        super().__init__()

        try:
            getattr(self, 'first')
        except AttributeError:
            self.guilds = set()
            self.channels = set()
            self.users = set()
            self.first = False

    def get(self, identifier: 'objects.Snowflake'):
        '''Return a given object with an given identifier if we know about it.'''
        for x in self.guilds:
            if identifier == x.id:
                return x
        for x in self.channels:
            if identifier == x.id:
                return x
        for x in self.users:
            if identifier == x.id:
                return x
        raise LookupError(f'Identifier {identifier} not in cache.')

    def add(self, object):
        '''Given some generic object, insert it into the cache.'''
        # Convert to dict
        # if type(object) is objects.Guild:
        #     self.guilds.add(object)
        # elif isinstance(object, objects.Channel):
        #     self.channels.add(object)
        # elif type(object) is objects.User:
        #     self.users.add(object)

    def clear(self):
        '''Remove all current elements within the cache.'''
        self.guilds = set()
        self.channels = set()
        self.users = set()
