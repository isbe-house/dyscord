from typing import Union, Optional
from abc import ABC

from .. import utilities
from ..client import api
from . import snowflake, message as ext_message, enumerations


class Channel(ABC):
    '''Abstract base class for Channels.'''

    _log = utilities.Log()

    CHANNEL_TYPES = enumerations.CHANNEL_TYPES

    id: 'snowflake.Snowflake'
    name: str
    position: int
    type: 'enumerations.CHANNEL_TYPES'

    def __str__(self):
        '''Return string representation.'''
        return f'{self.__class__.__name__}(name=\'{self.name}\', type={self.type.name})'

    def __repr__(self):
        '''Return string representation.'''
        return self.__str__()

    def cache(self):
        '''Deprecated caching function.'''
        utilities.Cache().add(self)

    def ingest_raw_dict(self, data, parent_guild=None):
        '''Parse a Channel from an API compliant dict.'''
        raise NotImplementedError()

    def from_dict(self, data, parent_guild=None) -> 'Channel':
        '''Parse a Channel from an API compliant dict.'''
        self.id = snowflake.Snowflake(data['id'])
        self.type = self.CHANNEL_TYPES(data['type'])
        self.name = data.get('name', '<DirectMessage>')
        return self

    @classmethod
    async def get_channel(cls, channel_id: snowflake.Snowflake):
        '''Invoke cache or API to get a channel of given channel_id.'''
        return ChannelImporter().ingest_raw_dict(await api.API.get_channel(channel_id))


class TextChannel(Channel):
    '''Text channel. May be public or private depending on privacy settings.'''

    guild_id: 'snowflake.Snowflake'
    # permission_overwrites: list
    rate_limit_per_user: int
    nsfw: Optional[bool]
    topic: str
    last_message_id: 'snowflake.Snowflake'
    parent_id: 'snowflake.Snowflake'
    default_auto_archive_duration: int

    def ingest_raw_dict(self, data, parent_guild=None) -> "TextChannel":
        '''Parse a TextChannel from an API compliant dict.'''
        super().from_dict(data, parent_guild)
        self.from_dict(data, parent_guild=None)

        self.cache()
        return self

    def from_dict(self, data, parent_guild=None):
        '''Parse a TextChannel from an API compliant dict.'''
        self.id = snowflake.Snowflake(data['id'])
        if 'guild_id' in data:
            self.guild_id = snowflake.Snowflake(data['guild_id'])
        self.name = data['name']
        self.type = enumerations.CHANNEL_TYPES(data['type'])
        if 'position' in data:
            self.position = data['position']
        if 'rate_limit_per_user' in data:
            self.rate_limit_per_user = data['rate_limit_per_user']
        if 'nsfw' in data:
            self.nsfw = data['nsfw']
        if 'topic' in data:
            self.topic = data['topic']
        if 'last_message_id' in data:
            self.last_message_id = snowflake.Snowflake(data['last_message_id'])
        if 'parent_id' in data:
            self.parent_id = snowflake.Snowflake(data['parent_id'])
        if 'default_auto_archive_duration' in data:
            self.default_auto_archive_duration = data['default_auto_archive_duration']
        return self

    async def send_message(self, message: Union[ext_message.Message, str]) -> 'ext_message.Message':
        '''Send message to this channel. Will also accept a string.'''
        if type(message) is ext_message.Message:
            message.validate()
        elif type(message) is str:
            new_message = ext_message.Message()
            new_message.content = message
            message = new_message
        else:
            raise TypeError(f'send_message given invalid input of [{type(message)}].')

        data = await api.API.create_message(self.id, message.to_sendable_dict())
        return ext_message.Message().from_dict(data)


class NewsChannel(Channel):
    '''News channel.'''

    def ingest_raw_dict(self, data, parent_guild=None) -> "NewsChannel":
        '''Parse a NewsChannel from an API compliant dict.'''
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class VoiceChannel(Channel):
    '''Voice channel.'''

    def ingest_raw_dict(self, data, parent_guild=None) -> "VoiceChannel":
        '''Parse a VoiceChannel from an API compliant dict.'''
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class DMChannel(Channel):
    '''Direct Message with a specific user.'''

    def ingest_raw_dict(self, data, parent_guild=None) -> "DMChannel":
        '''Parse a Channel from an API compliant dict, then return the appropriate subclass object.'''
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class GroupDMChannel(Channel):
    '''DM with several users.'''

    def ingest_raw_dict(self, data, parent_guild=None) -> "GroupDMChannel":
        '''Parse a Channel from an API compliant dict, then return the appropriate subclass object.'''
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class GuildPublicThread(Channel):
    '''Public thread.'''

    def ingest_raw_dict(self, data, parent_guild=None) -> "GuildPublicThread":
        '''Parse a Channel from an API compliant dict, then return the appropriate subclass object.'''
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class GuildPrivateThread(Channel):
    '''Private thread.'''

    def ingest_raw_dict(self, data, parent_guild=None) -> "GuildPrivateThread":
        '''Parse a Channel from an API compliant dict, then return the appropriate subclass object.'''
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class CategoryChannel(Channel):
    '''Not a text channel, used for grouping servers in discord's GUI.'''

    def ingest_raw_dict(self, data, parent_guild=None) -> "CategoryChannel":
        '''Parse a Channel from an API compliant dict, then return the appropriate subclass object.'''
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class StoreChannel(Channel):
    '''Channel to sell things in.'''

    def ingest_raw_dict(self, data, parent_guild=None) -> "StoreChannel":
        '''Parse a Channel from an API compliant dict, then return the appropriate subclass object.'''
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class ChannelImporter:
    '''Dynamic Channel identifier and parser.'''

    @classmethod
    def ingest_raw_dict(cls, data, parent_guild=None) -> 'Channel':
        '''Parse a Channel from an API compliant dict, then return the appropriate subclass object.'''
        return cls.from_dict(data, parent_guild)

    @classmethod
    def from_dict(cls, data, parent_guild=None) -> 'Union[TextChannel, DMChannel, VoiceChannel, GroupDMChannel, GuildPublicThread, GuildPrivateThread, CategoryChannel, NewsChannel, StoreChannel]':
        '''Parse a Channel from an API compliant dict, then return the appropriate subclass object.'''
        new_channel: Union[TextChannel,
                           DMChannel,
                           VoiceChannel,
                           GroupDMChannel,
                           GuildPublicThread,
                           GuildPrivateThread,
                           CategoryChannel,
                           NewsChannel,
                           StoreChannel,
                           ]

        if data["type"] == Channel.CHANNEL_TYPES.GUILD_TEXT:
            new_channel = TextChannel()

        elif data["type"] == Channel.CHANNEL_TYPES.DM:
            new_channel = DMChannel()

        elif data["type"] == Channel.CHANNEL_TYPES.GUILD_VOICE:
            new_channel = VoiceChannel()

        elif data["type"] == Channel.CHANNEL_TYPES.GROUP_DM:
            new_channel = GroupDMChannel()

        elif data["type"] == Channel.CHANNEL_TYPES.GUILD_PUBLIC_THREAD:
            new_channel = GuildPublicThread()

        elif data["type"] == Channel.CHANNEL_TYPES.GUILD_PRIVATE_THREAD:
            new_channel = GuildPrivateThread()

        elif data["type"] == Channel.CHANNEL_TYPES.GUILD_CATEGORY:
            new_channel = CategoryChannel()

        elif data["type"] == Channel.CHANNEL_TYPES.GUILD_NEWS:
            new_channel = NewsChannel()

        elif data["type"] == Channel.CHANNEL_TYPES.GUILD_STORE:
            new_channel = StoreChannel()

        else:
            raise ValueError(f'Dict contained unknown channel type. {data["type"]}, {Channel.CHANNEL_TYPES(data["type"]).name}')

        new_channel.from_dict(data, parent_guild)

        return new_channel
