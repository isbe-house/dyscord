from .. import objects
from .borg import Borg


class Cache(Borg):
    '''
    Generic cache of objects we have been told about from the API.
    '''

    def __init__(self):
        super().__init__()

        try:
            getattr(self, 'first')
        except AttributeError:
            self.guilds = set()
            self.channels = set()
            self.users = set()
            self.first = False

    def get(self, identifier):
        '''
        Return a given object with an given identifier if we know about it.
        '''
        for x in self.guilds:
            if identifier == x.id:
                return x

    def add(self, object):
        '''
        Given some generic object, insert it into the cache.
        '''

        if type(object) is objects.Guild:
            self.guilds.add(object)

    def clear(self):

        self.guilds = set()
        self.channels = set()
        self.users = set()
