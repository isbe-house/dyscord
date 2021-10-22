import asyncio
import datetime
import enum
from typing import Union, Optional, List, Dict

from .base_object import BaseDiscordObject
from . import user, channel as ext_channel, snowflake, enumerations, embed as ext_embed, guild as ext_guild, role as ext_role
from ..utilities import cache, log
from .interactions import components as ext_components

from ..client import api


class Message(BaseDiscordObject, ext_components.ComponentAdder, ext_embed.EmbedAdder):
    '''Message containing infomation about it's content, origin, authors, etc.'''

    _log = log.Log()

    MESSAGE_TYPE = enumerations.MESSAGE_TYPE

    id: 'snowflake.Snowflake' = None  # type: ignore
    channel_id: 'snowflake.Snowflake' = None  # type: ignore
    guild_id: Optional['snowflake.Snowflake'] = None  # type: ignore
    guild: Optional['ext_guild.Guild'] = None  # type: ignore
    author: 'user.User' = None  # type: ignore
    member: Optional['user.Member'] = None  # type: ignore
    content: str = None  # type: ignore
    timestamp: datetime.datetime = None  # type: ignore
    edited_timestamp: Optional[datetime.datetime] = None  # type: ignore
    tts: bool = None  # type: ignore
    mention_everyone: bool = None  # type: ignore
    mentions: List['user.User'] = None  # type: ignore
    mention_roles: List['ext_role.Role'] = None  # type: ignore # Roles are TBD
    mention_channels: List['ext_channel.Channel'] = None  # type: ignore
    attachments: 'List' = None  # type: ignore # attachment.Attachment TDB
    embeds: Optional[List[ext_embed.Embed]] = None  # type: ignore
    # reactions: 'List[reaction.Reaction]'  = None  # type: ignore
    nonce: Optional[Union[int, str]] = None  # type: ignore
    pinned: bool = None  # type: ignore
    webhook_id: Optional['snowflake.Snowflake'] = None  # type: ignore
    type: 'enumerations.MESSAGE_TYPE' = None  # type: ignore
    # activity = None  # Activity TBD = None  # type: ignore
    # application: application.Application = None  # Application TBD = None  # type: ignore
    application_id: 'snowflake.Snowflake' = None  # type: ignore
    # message_reference: 'MessageReference' = None  # Message Reference TBD = None  # type: ignore
    flags: int  # Message Flags = None  # type: ignore
    referenced_message: 'Message' = None  # type: ignore
    # interaction = None  # Interactions TBD = None  # type: ignore
    thread: 'ext_channel.Channel' = None  # type: ignore
    components: List['ext_components.Component']  # Message components TBD = None  # type: ignore
    # sticker_items: List[Sticker] = []  # Stickers TBD = None  # type: ignore

    def __init__(self,
                 content: str = None
                 ):
        '''Init.'''
        if content is not None:
            self.content = content

    def __getattr__(self, name):
        '''Do dynamic lookup on various fields that may not be populated, but have valid representations in the API.'''
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
        '''Ingest and cache a given object for future use.'''
        self.from_dict(data)

        # I do not believe we need to cache these at this time.
        # self.cache()
        return self

    def from_dict(self, data: dict) -> 'Message':
        '''Parse a Message from an API compliant dict.'''
        # Mandatory Fields
        self.attachments = list()
        if 'attachments' in data:
            for attachment in data['attachments']:
                self.attachments.append(attachment)
        self.author = user.User().from_dict(data['author'])  # TODO: Update after we can parse in users.
        self.channel_id = snowflake.Snowflake(data['channel_id'])
        self.components = list()
        for component in data['components']:
            self.components.append(component)
        self.content = data['content']
        self.edited_timestamp = datetime.datetime.fromisoformat(data['edited_timestamp']) if data['edited_timestamp'] is not None else None
        self.embeds = list()
        for embed in data['embeds']:
            self.embeds.append(embed)
        self.flags = data['flags']
        self.id = snowflake.Snowflake(data['id'])
        self.mention_everyone = data['mention_everyone']
        self.mention_roles = []
        for role in data['mention_roles']:
            # self.mention_roles.append(role.Role().from_dict(role))
            pass
        self.mentions = []
        for user_dict in data['mentions']:
            self.mentions.append(user.User().from_dict(user_dict))
        self.pinned = data['pinned']
        self.timestamp = datetime.datetime.fromisoformat(data['timestamp'])
        self.tts = data['tts']
        self.type = enumerations.MESSAGE_TYPE(data['type'])

        # Optional fields
        self.guild_id = snowflake.Snowflake(data['guild_id']) if (data.get('guild_id', None) is not None) else None
        if 'member' in data:
            self.member = user.Member().from_dict(data['member'])  # TODO: Update after we can parse in users.
            self.member.update_from_user(self.author)
        self.nonce = data['nonce'] if 'nonce' in data else None
        self.webhook_id = snowflake.Snowflake(data['webhook_id']) if (data.get('webhook_id', None) is not None) else None

        return self

    def cache(self):
        '''Sav object to the cache for faster recall in the future.'''
        raise NotImplementedError(f'{__class__.__name__} does not yet implement this function.')

    def to_sendable_dict(self) -> dict:
        '''Sending a message only allows a subset of attributes. Ignore anything else about this message when producing that dict.'''
        new_dict: Dict[str, object] = dict()
        if self.content is not None:
            new_dict['content'] = self.content
        new_dict['tts'] = self.tts if hasattr(self, 'tts') else False
        # new_dict['file'] = None  # TODO: Handle a file upload.
        if self.embeds is not None:
            new_dict['embeds'] = list()  # TODO: Handle embeds.
            assert type(new_dict['embeds']) is list
            assert type(self.embeds) is list
            for embed in self.embeds:
                new_dict['embeds'].append(embed.to_dict())
        # new_dict['allowed_mentions'] = True  # BUG: This isn't a bool, its an `AllowedMentionsObject`, which we don't support yet.
        # new_dict['message_reference'] = None
        # new_dict['sticker_ids'] = None

        if isinstance(self.components, list) and len(self.components):
            new_dict['components'] = list()
            assert type(new_dict['components']) is list
            for component in self.components:
                new_dict['components'].append(component.to_dict())

        return new_dict

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
        assert (self.content is not None) or (self.embeds is not None) or (self.attachments is not None),\
            'Message must have a content, embeds, or attachments to be valid for sending.'

        if self.content is not None:
            assert type(self.content) is str,\
                f'Got invalid type {type(self.content)} in Message.content, must be str.'

            assert len(self.content) <= 2000,\
                f'Invalid length of {len(self.content):,} in Message.content, must be <= 2000 characters.'

        if self.components is not None:
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
                    if sub_component.custom_id is not None:
                        assert sub_component.custom_id not in custom_ids,\
                            f'Found duplicate custom_id [{sub_component.custom_id}]'
                        custom_ids.append(sub_component.custom_id)

        if self.embeds is not None:
            assert type(self.embeds) is list,\
                f'Got invalid type {type(self.embeds)} in Message.embeds, must be list.'

            assert len(self.embeds) <= 25,\
                f'Invalid length of {len(self.embeds):,} in Message.embeds, must be <= 5 elements.'

            for embed in self.embeds:
                embed.validate()

    class formatter:
        '''Helper formatting functions.'''

        class TIMESTAMP_FLAGS(enum.Enum):
            '''Types of timestamp displays.'''
            SHORT_TIME = 't'
            LONG_TIME = 'T'
            SHORT_DATE = 'd'
            LONG_DATE = 'D'
            DEFAULT = 'f'
            LONG_DATE_TIME = 'F'
            RELATIVE_TIME = 'R'

        @classmethod
        def timestamp(cls, timestamp: datetime.datetime, flag: Union[TIMESTAMP_FLAGS, str] = TIMESTAMP_FLAGS.DEFAULT) -> str:
            '''Return valid timestamp string. Discord will display this in a useful way.'''
            if type(flag) is cls.TIMESTAMP_FLAGS:
                flag = flag.value
            return f'<t:{int(timestamp.timestamp())}:{flag}>'

        @classmethod
        def user(cls, user_id: snowflake.Snowflake):
            '''Return valid mention string for the user's name.'''
            return f'<@{user_id}>'

        @classmethod
        def user_nickname(cls, user_id: snowflake.Snowflake):
            '''Return valid mention string for the user's nickname.'''
            return f'<@!{user_id}>'


class MessageReference(BaseDiscordObject):
    '''Slim data holding class.'''

    message_id: Optional[snowflake.Snowflake] = None  # id of the originating message
    channel_id: Optional[snowflake.Snowflake] = None  # id of the originating message's channel
    guild_id: Optional[snowflake.Snowflake] = None  # id of the originating message's guild
    fail_if_not_exists: Optional[bool] = None  # when sending, whether to error if the referenced message doesn't exist instead of sending as a normal (non-reply) message, default true
