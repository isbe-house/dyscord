import datetime
from typing import Union


class Snowflake:

    DISCORD_EPOCH = 1420070400000

    def __init__(self, identifier: Union[int, str, 'Snowflake'] = None):
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
        return str(self.identifier)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if type(other) in [str, int]:
            other = Snowflake(other)
        elif type(other) is Snowflake:
            pass
        else:
            return NotImplemented

        return self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)

    @property
    def timestamp(self):
        assert type(self.identifier) is int

        return ((self.identifier >> 22) + 1420070400000) / 1000

    @property
    def worker_id(self):
        assert type(self.identifier) is int

        return (self.identifier & 0x3E0000) >> 17

    @property
    def process_id(self):
        assert type(self.identifier) is int

        return (self.identifier & 0x1F000) >> 12

    @property
    def increment(self):
        assert type(self.identifier) is int

        return self.identifier & 0xFFF

    def generate(self):
        self.identifier = (int(datetime.datetime.now().timestamp() * 1000) - 1420070400000) << 22
