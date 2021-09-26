import enum

from .. import utilities
from ..client import api
from . import snowflake


class Channel:

    _log = utilities.Log()

    class ChannelTypes(enum.IntEnum):
        GUILD_TEXT = 0  # a text channel within a server
        DM = 1  # a direct message between users
        GUILD_VOICE = 2  # a voice channel within a server
        GROUP_DM = 3  # a direct message between multiple users
        GUILD_CATEGORY = 4  # an organizational category that contains up to 50 channels
        GUILD_NEWS = 5  # a channel that users can follow and crosspost into their own server
        GUILD_STORE = 6  # a channel in which game developers can sell their game on Discord
        GUILD_NEWS_THREAD = 10  # a temporary sub-channel within a GUILD_NEWS channel
        GUILD_PUBLIC_THREAD = 11  # a temporary sub-channel within a GUILD_TEXT channel
        GUILD_PRIVATE_THREAD = 12  # a temporary sub-channel within a GUILD_TEXT channel that is only viewable by those invited and those with the MANAGE_THREADS permission
        GUILD_STAGE_VOICE = 13  # a voice channel for hosting events with an audience

    def __init__(self):
        self.id: snowflake.Snowflake
        self.name: str
        self.position: int
        self.type: Channel.ChannelTypes

    def __str__(self):
        return f'{self.__class__.__name__}(name=\'{self.name}\', type={self.type.name})'

    def __repr__(self):
        return self.__str__()

    def cache(self):
        # Preventing circular imports

        utilities.Cache().add(self)

    def ingest_raw_dict(self, data, parent_guild=None):
        raise NotImplementedError()

    def from_dict(self, data, parent_guild=None):
        self.id = snowflake.Snowflake(data['id'])
        self.type = self.ChannelTypes(data['type'])
        return self

    def get_channel(self, channel_id: snowflake.Snowflake):
        return ChannelImporter().ingest_raw_dict(api.API.get_channel(channel_id))


class TextChannel(Channel):

    def ingest_raw_dict(self, data, parent_guild=None) -> "TextChannel":
        super().from_dict(data, parent_guild)
        self.from_dict(data, parent_guild=None)

        self._log.debug("Ingest called.")
        self.cache()
        return self

    def from_dict(self, data, parent_guild=None):
        return self


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
        new_channel: Channel

        if data["type"] == Channel.ChannelTypes.GUILD_TEXT:
            new_channel = TextChannel()

        elif data["type"] == Channel.ChannelTypes.DM:
            new_channel = DMChannel()

        elif data["type"] == Channel.ChannelTypes.GUILD_VOICE:
            new_channel = VoiceChannel()

        elif data["type"] == Channel.ChannelTypes.GROUP_DM:
            new_channel = GroupDMChannel()

        elif data["type"] == Channel.ChannelTypes.GUILD_PUBLIC_THREAD:
            new_channel = GuildPublicThread()

        elif data["type"] == Channel.ChannelTypes.GUILD_PRIVATE_THREAD:
            new_channel = GuildPrivateThread()

        elif data["type"] == Channel.ChannelTypes.GUILD_CATEGORY:
            new_channel = CategoryChannel()

        elif data["type"] == Channel.ChannelTypes.GUILD_NEWS:
            new_channel = NewsChannel()

        elif data["type"] == Channel.ChannelTypes.GUILD_STORE:
            new_channel = StoreChannel()

        else:
            raise ValueError(f'Dict contained unknown channel type. {data["type"]}, {Channel.ChannelTypes(data["type"]).name}')

        new_channel.ingest_raw_dict(data, parent_guild)

        return new_channel
