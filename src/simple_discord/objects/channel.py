from typing import Union, Optional

from .. import utilities
from ..client import api
from . import snowflake, message as ext_message, enumerations


class Channel:

    _log = utilities.Log()

    CHANNEL_TYPES = enumerations.CHANNEL_TYPES

    id: 'snowflake.Snowflake'
    name: str
    position: int
    type: 'enumerations.CHANNEL_TYPES'

    def __str__(self):
        return f'{self.__class__.__name__}(name=\'{self.name}\', type={self.type.name})'

    def __repr__(self):
        return self.__str__()

    def cache(self):
        utilities.Cache().add(self)

    def ingest_raw_dict(self, data, parent_guild=None):
        raise NotImplementedError()

    def from_dict(self, data, parent_guild=None):
        self.id = snowflake.Snowflake(data['id'])
        self.type = self.CHANNEL_TYPES(data['type'])
        self.name = data.get('name', '<DirectMessage>')
        return self

    @classmethod
    async def get_channel(cls, channel_id: snowflake.Snowflake):
        return ChannelImporter().ingest_raw_dict(await api.API.get_channel(channel_id))


class TextChannel(Channel):

    guild_id: 'snowflake.Snowflake'
    # permission_overwrites: list
    rate_limit_per_user: int
    nsfw: Optional[bool]
    topic: str
    last_message_id: 'snowflake.Snowflake'
    parent_id: 'snowflake.Snowflake'
    default_auto_archive_duration: int

    def ingest_raw_dict(self, data, parent_guild=None) -> "TextChannel":
        super().from_dict(data, parent_guild)
        self.from_dict(data, parent_guild=None)

        self.cache()
        return self

    def from_dict(self, data, parent_guild=None):
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

    def ingest_raw_dict(self, data, parent_guild=None) -> "NewsChannel":
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class VoiceChannel(Channel):

    def ingest_raw_dict(self, data, parent_guild=None) -> "VoiceChannel":
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class DMChannel(Channel):

    def ingest_raw_dict(self, data, parent_guild=None) -> "DMChannel":
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class GroupDMChannel(Channel):

    def ingest_raw_dict(self, data, parent_guild=None) -> "GroupDMChannel":
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class GuildPublicThread(Channel):

    def ingest_raw_dict(self, data, parent_guild=None) -> "GuildPublicThread":
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class GuildPrivateThread(Channel):

    def ingest_raw_dict(self, data, parent_guild=None) -> "GuildPrivateThread":
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class CategoryChannel(Channel):

    def ingest_raw_dict(self, data, parent_guild=None) -> "CategoryChannel":
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class StoreChannel(Channel):

    def ingest_raw_dict(self, data, parent_guild=None) -> "StoreChannel":
        super().from_dict(data, parent_guild)

        self._log.debug("Ingest called.")
        self.cache()
        return self


class ChannelImporter:
    @classmethod
    def ingest_raw_dict(cls, data, parent_guild=None) -> "Channel":
        return cls.from_dict(data, parent_guild)

    @classmethod
    def from_dict(cls, data, parent_guild=None) -> "Channel":
        new_channel: Channel

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
