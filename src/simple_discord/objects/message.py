import asyncio
import datetime
import enum
from typing import Union, Optional, List, Dict

from .base_object import BaseDiscordObject
from . import user, channel as ext_channel, snowflake, enumerations, embed as ext_embed, guild as ext_guild
from ..utilities import cache, log
from .interactions import components as ext_components

from ..client import api


class Message(BaseDiscordObject, ext_components.ComponentAdder, ext_embed.EmbedAdder):
    '''Message containing infomation about it's content, origin, authors, etc.'''

    _log = log.Log()

    MESSAGE_TYPE = enumerations.MESSAGE_TYPE

    id: 'snowflake.Snowflake'
    channel_id: 'snowflake.Snowflake'
    guild_id: Optional['snowflake.Snowflake']
    guild: Optional['ext_guild.Guild']
    author: 'user.User'
    member: Optional['user.Member']
    content: str
    timestamp: datetime.datetime
    edited_timestamp: Optional[datetime.datetime]
    tts: bool
    mention_everyone: bool
    mentions: List['user.User']
    # mention_roles: list[role.Role]  # Roles are TBD
    mention_channels: List['ext_channel.Channel']
    # attachments: list[attachment.Attachment]  # Attachments are TBD
    embeds: Optional[List[ext_embed.Embed]]
    # reactions: list[reaction.Reaction]  # Reactions are TBD
    nonce: Optional[Union[int, str]]
    pinned: bool
    webhook_id: Optional['snowflake.Snowflake']
    type: 'enumerations.MESSAGE_TYPE'
    # activity = None  # Activity TBD
    # application: application.Application = None  # Application TBD
    application_id: 'snowflake.Snowflake'
    # message_reference: = None  # Message Reference TBD
    # flags = None  # Message Flags TBD
    referenced_message: 'Message'
    # interaction = None  # Interactions TBD
    thread: 'ext_channel.Channel'
    components: List['ext_components.Component']  # Message components TBD
    # sticker_items: List[Sticker] = []  # Stickers TBD

    def __init__(self,
                 content: str = None
                 ):
        if content is not None:
            self.content = content

    def __getattr__(self, name):

        if name == 'channel' and 'channel_id' in self.__dict__:
            try:
                channel = cache.Cache().get(self.channel_id)
                self._log.info('Got channel from the cache.')
            except LookupError:
                loop = asyncio.get_event_loop()
                channel_dict = loop.run_until_complete(api.API.get_channel(self.channel_id))
                channel = ext_channel.ChannelImporter().ingest_raw_dict(channel_dict)
                self._log.info('Got channel from the API.')
            self.channel = channel
            return channel

        if name == 'guild' and 'guild_id' in self.__dict__:
            assert type(self.guild_id) is snowflake.Snowflake
            try:
                guild = cache.Cache().get(self.guild_id)
                self._log.info('Got guild from the cache.')
            except LookupError:
                loop = asyncio.get_event_loop()
                guild_dict = loop.run_until_complete(api.API.get_guild(self.guild_id))
                guild = ext_guild.Guild().from_dict(guild_dict)
                self._log.info('Got guild from the API.')
            self.guild = guild
            return guild
        raise AttributeError(f'Failed to find \'{name}\'')

    def ingest_raw_dict(self, data) -> 'Message':
        '''
        Ingest and cache a given object for future use.
        '''
        self.from_dict(data)

        # I do not believe we need to cache these at this time.
        # self.cache()
        return self

    def from_dict(self, data) -> 'Message':
        '''
        Parse an object from a dictionary and return it.
        '''

        self.id = snowflake.Snowflake(data['id'])
        self.channel_id = snowflake.Snowflake(data['channel_id'])
        self.guild_id = snowflake.Snowflake(data['guild_id']) if (data.get('guild_id', None) is not None) else None
        self.author = user.User().from_dict(data['author'])  # TODO: Update after we can parse in users.
        if 'member' in data:
            self.member = user.Member().from_dict(data['member'])  # TODO: Update after we can parse in users.
            self.member.update_from_user(self.author)
        self.content = data['content']
        self.timestamp = datetime.datetime.fromisoformat(data['timestamp'])
        self.edited_timestamp = datetime.datetime.fromisoformat(data['edited_timestamp']) if data['edited_timestamp'] is not None else None
        self.tts = data['tts']
        self.mention_everyone = data['mention_everyone']

        self.mentions = []
        for user_dict in data['mentions']:
            self.mentions.append(user.User().from_dict(user_dict))

        self.nonce = data['nonce'] if 'nonce' in data else None
        self.pinned = data['pinned']
        self.webhook_id = snowflake.Snowflake(data['webhook_id']) if (data.get('webhook_id', None) is not None) else None
        self.type = enumerations.MESSAGE_TYPE(data['type'])

        return self

    def cache(self):
        '''
        Sav object to the cache for faster recall in the future.
        '''
        raise NotImplementedError(f'{__class__.__name__} does not yet implement this function.')

    def to_sendable_dict(self) -> dict:
        '''
        Sending a message only allows a subset of attributes. Ignore anything else about this message when producing that dict.
        '''
        new_dict: Dict[str, object] = dict()
        new_dict['content'] = self.content if hasattr(self, 'content') else None
        new_dict['tts'] = self.tts if hasattr(self, 'tts') else False
        # new_dict['file'] = None  # TODO: Handle a file upload.
        if hasattr(self, 'embeds'):
            new_dict['embeds'] = list()  # TODO: Handle embeds.
            assert type(new_dict['embeds']) is list
            assert type(self.embeds) is list
            for embed in self.embeds:
                new_dict['embeds'].append(embed.to_dict())
        # new_dict['allowed_mentions'] = True  # BUG: This isn't a bool, its an `AllowedMentionsObject`, which we don't support yet.
        # new_dict['message_reference'] = None
        # new_dict['sticker_ids'] = None

        if hasattr(self, 'components') and type(self.components) is list and len(self.components):
            new_dict['components'] = list()
            assert type(new_dict['components']) is list
            for component in self.components:
                new_dict['components'].append(component.to_dict())

        return new_dict

    def validate(self):
        '''
        Validate a message for sending to discord.
        '''
        assert hasattr(self, 'content') or hasattr(self, 'embeds') or hasattr(self, 'file'),\
            'Message must have a content, embeds, or file to be valid for sending.'

        if hasattr(self, 'content'):
            assert type(self.content) is str,\
                f'Got invalid type {type(self.content)} in Message.content, must be str.'

            assert len(self.content) <= 2000,\
                f'Invalid length of {len(self.content):,} in Message.content, must be <= 2000 characters.'

        if hasattr(self, 'components'):
            assert type(self.components) is list,\
                f'Got invalid type {type(self.components)} in Message.components, must be list.'

            assert len(self.components) <= 5,\
                f'Invalid length of {len(self.components):,} in Message.components, must be <= 5 elements.'

            custom_ids = list()
            for component in self.components:
                assert type(component) is ext_components.ActionRow,\
                    f'Got invalid type {type(component)} in Message.components, must be ActionRow.'
                component.validate()
                for sub_component in component.components:
                    if hasattr(sub_component, 'custom_id'):
                        assert sub_component.custom_id not in custom_ids,\
                            f'Found duplicate custom_id [{sub_component.custom_id}]'
                        custom_ids.append(sub_component.custom_id)

        if hasattr(self, 'embeds'):
            assert type(self.embeds) is list,\
                f'Got invalid type {type(self.embeds)} in Message.embeds, must be list.'

            assert len(self.embeds) <= 25,\
                f'Invalid length of {len(self.embeds):,} in Message.embeds, must be <= 5 elements.'

            for embed in self.embeds:
                embed.validate()

    class formatter:

        class TIMESTAMP_FLAGS(enum.Enum):
            SHORT_TIME = 't'
            LONG_TIME = 'T'
            SHORT_DATE = 'd'
            LONG_DATE = 'D'
            DEFAULT = 'f'
            LONG_DATE_TIME = 'F'
            RELATIVE_TIME = 'R'

        @classmethod
        def timestamp(cls, timestamp: datetime.datetime, flag: Union[TIMESTAMP_FLAGS, str] = TIMESTAMP_FLAGS.DEFAULT) -> str:
            if type(flag) is cls.TIMESTAMP_FLAGS:
                flag = flag.value
            return f'<t:{int(timestamp.timestamp())}:{flag}>'

        @classmethod
        def user(cls, user_id: snowflake.Snowflake):
            return f'<@{user_id}>'

        @classmethod
        def user_nickname(cls, user_id: snowflake.Snowflake):
            return f'<@!{user_id}>'
