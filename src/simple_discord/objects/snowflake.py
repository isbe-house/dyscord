import datetime
from typing import Union


class Snowflake:
    '''Discord specific UUID like object. Generally interchangable with a string contained the same sequence of characters.'''

    DISCORD_EPOCH = 1420070400000

    def __init__(self, identifier: Union[int, str, 'Snowflake'] = None):
        '''Initialize the Snowflake.

        Arguments:
            identifier (int, str, Snowflake): Identifier to base off of.
        '''
        self.identifier: int

        if type(identifier) is int:
            self.identifier = identifier
        elif type(identifier) is str:
            self.identifier = int(identifier)
        elif type(identifier) is Snowflake:
            self.identifier = identifier.identifier
        else:
            self.generate()

        assert type(self.identifier) is int

    def __str__(self):
        '''Return string representation.'''
        return str(self.identifier)

    def __repr__(self):
        '''Return string representation.'''
        return self.__str__()

    def __eq__(self, other):
        '''Determine if other is equivalent to this Snowflake..'''
        if type(other) in [str, int]:
            other = Snowflake(other)
        elif type(other) is Snowflake:
            pass
        else:
            return NotImplemented

        return self.identifier == other.identifier

    def __hash__(self):
        '''Hash.'''
        return hash(self.identifier)

    @property
    def timestamp(self):
        '''The timestamp of the Snowflake.'''
        assert type(self.identifier) is int

        return ((self.identifier >> 22) + 1420070400000) / 1000

    @property
    def worker_id(self):
        '''The worker ID that generated the Snowflake.'''
        assert type(self.identifier) is int

        return (self.identifier & 0x3E0000) >> 17

    @property
    def process_id(self):
        '''The process ID of the Snowflake.'''
        assert type(self.identifier) is int

        return (self.identifier & 0x1F000) >> 12

    @property
    def increment(self):
        '''The increment sequence count of the Snowflake.'''
        assert type(self.identifier) is int

        return self.identifier & 0xFFF

    def generate(self):
        '''Generate a fake Snowflake locally.'''
        self.identifier = (int(datetime.datetime.now().timestamp() * 1000) - 1420070400000) << 22
