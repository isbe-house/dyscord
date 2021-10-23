import asyncio
import datetime
import enum
from typing import Union, Optional, List, Dict

from .base_object import BaseDiscordObject
from . import snowflake, enumerations
from . import user as ext_user,\
    channel as ext_channel,\
    embed as ext_embed,\
    guild as ext_guild,\
    role as ext_role
from ..utilities import log
from .interactions import components as ext_components

from ..client import api


class Message(BaseDiscordObject, ext_components.ComponentAdder, ext_embed.EmbedAdder):
    '''Message containing infomation about it's content, origin, authors, etc.

    Attributes:
        id (Snowflake): Unique ID of the message.
        channel_id (Snowflake): Unique ID of the channel the message came from.
        guild_id (Snowflake|None): Unique ID of the channel the message came from. Defaults to None.
        guild (Guild|None): Actual guild object item is from. This will autopopulate from the API if it is not present.
        author (User): The author of the message.
        member (Member): If the message was in a guild, this will be the Member object of the author.
        content (str): The actual content of the message.
        timestamp (datetime): Date and time the message was posted.
        edited_timestamp (datetime|None): If the message has been edited, this is the date and time it was.
        tts (bool): Text to speech flag.
        mention_everyone (bool): Message had an @everyone in it.
        mentions ([User]): List of mentioned User.
        mention_roles ([Role]): List of mentioned Role.
        mention_channels ([Channel]): List of mentioned Channel. Note that each channel will be the correct type.
        embeds ([Embed]): List of rich Embed objects.
        nonce (str|None): Nonce used to send the message.
        pinned (bool): True if message is pinned in the channel.
        webhook_id (Snowflake|None): ID of the webhook used to send this message.
        type (MESSAGE_TYPE): Enumeration of the type of message.
        application_id (Snowflake|None): ID of the application that send the message.
        message_reference (MessageReference|None): data showing the source of a crosspost, channel follow add, pin, or reply message
        flags (int): Bitfield of message flags.
        referenced_message (Message|None): Message object refereed to in message_reference.
        thread (Channel): Thread the message is a part of.
        components ([Component]): List of components in the message if it is an interaction.
    '''

    _log = log.Log()

    MESSAGE_TYPE = enumerations.MESSAGE_TYPE

    id: 'snowflake.Snowflake' = None  # type: ignore
    channel_id: 'snowflake.Snowflake' = None  # type: ignore
    guild_id: Optional['snowflake.Snowflake'] = None  # type: ignore
    author: 'ext_user.User' = None  # type: ignore
    member: Optional['ext_user.Member'] = None  # type: ignore
    content: str = None  # type: ignore
    timestamp: datetime.datetime = None  # type: ignore
    edited_timestamp: Optional[datetime.datetime] = None  # type: ignore
    tts: bool = None  # type: ignore
    mention_everyone: bool = None  # type: ignore
    mentions: List['ext_user.User'] = None  # type: ignore
    mention_roles: List['ext_role.Role'] = None  # type: ignore
    mention_channels: List['ext_channel.Channel'] = None  # type: ignore
    attachments: 'List' = None  # type: ignore
    embeds: Optional[List[ext_embed.Embed]] = None  # type: ignore
    # reactions: 'List[reaction.Reaction]'  = None  # type: ignore
    nonce: Optional[Union[int, str]] = None  # type: ignore
    pinned: bool = None  # type: ignore
    webhook_id: Optional['snowflake.Snowflake'] = None  # type: ignore
    type: 'enumerations.MESSAGE_TYPE' = None  # type: ignore
    # activity = None  # Activity TBD = None  # type: ignore
    # application: application.Application = None  # Application TBD = None  # type: ignore
    application_id: 'Optional[snowflake.Snowflake]' = None  # type: ignore
    message_reference: 'Optional[MessageReference]' = None  # type: ignore
    flags: Optional[int]  # type: ignore
    referenced_message: 'Optional[Message]' = None  # type: ignore
    # interaction = None  # type: ignore
    thread: 'ext_channel.Channel' = None  # type: ignore
    components: List['ext_components.Component'] = None  # type: ignore
    # sticker_items: List[Sticker] = []  # type: ignore

    def __init__(self,
                 content: str = None
                 ):
        '''Init.'''
        if content is not None:
            self.content = content

    @property
    def channel(self):
        '''Attempt to grab channel from the API.'''
        if self.channel_id is None:
            return None
        loop = asyncio.get_event_loop()
        channel_dict = loop.run_until_complete(api.API.get_channel(self.channel_id))
        channel = ext_channel.ChannelImporter().from_dict(channel_dict)
        self._log.info('Got channel from the API.')
        return channel

    @property
    def guild(self):
        '''Attempt to grab guild from the API.'''
        if self.guild_id is None:
            return None
        loop = asyncio.get_event_loop()
        guild_dict = loop.run_until_complete(api.API.get_guild(self.guild_id))
        guild = ext_guild.Guild().from_dict(guild_dict)
        self._log.info('Got guild from the API.')
        return guild

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
        self.author = ext_user.User().from_dict(data['author'])  # TODO: Update after we can parse in users.
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
        self.mention_roles = list()
        for role in data['mention_roles']:
            # TODO: Roles are just ID's here, we need to parse them into actual role objects.
            # self.mention_roles.append(ext_role.Role().from_dict(role))
            pass
        self.mentions = list()
        for user_dict in data['mentions']:
            self.mentions.append(ext_user.User().from_dict(user_dict))
        self.pinned = data['pinned']
        self.timestamp = datetime.datetime.fromisoformat(data['timestamp'])
        self.tts = data['tts']
        self.type = enumerations.MESSAGE_TYPE(data['type'])

        # Optional fields
        self.guild_id = snowflake.Snowflake(data['guild_id']) if (data.get('guild_id', None) is not None) else None
        if 'member' in data:
            self.member = ext_user.Member().from_dict(data['member'])  # TODO: Update after we can parse in users.
            self.member.update_from_user(self.author)
        self.nonce = data['nonce'] if 'nonce' in data else None
        self.webhook_id = snowflake.Snowflake(data['webhook_id']) if (data.get('webhook_id', None) is not None) else None
        self.message_reference = MessageReference().from_dict(data['message_reference']) if ('message_reference' in data) and (data['message_reference'] is not None) else None
        self.referenced_message = Message().from_dict(data['referenced_message']) if ('referenced_message' in data) and (data['referenced_message'] is not None) else None
        self.mention_channels = list()
        if 'mention_channels' in data:
            for user_dict in data['mention_channels']:
                self.mention_channels.append(ext_channel.ChannelImporter().from_dict(user_dict))

        return self

    def cache(self):
        '''Save object to the cache for faster recall in the future.'''
        raise NotImplementedError(f'{__class__.__name__} does not yet implement this function.')

    def to_sendable_dict(self) -> dict:
        '''Sending a message only allows a subset of attributes. Ignore anything else about this message when producing that dict.'''
        new_dict: Dict[str, object] = dict()
        if self.content is not None:
            new_dict['content'] = self.content
        new_dict['tts'] = self.tts if (self.tts is not None) else False
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
        '''Helper formatting functions.

        These mostly implement the functions found in the [Discord API docs](https://discord.com/developers/docs/reference#message-formatting).


        Examples:
            When generating a string for a message, the formatter class provides a quick shortcut to get and use the various formatters.

            ```python
            message = Message()
            f'The time is {message.formatter.timestamp()}!'
            ```

        '''

        class TIMESTAMP_FLAGS(enum.Enum):
            '''Types of timestamp displays.

            Attributes:
                SHORT_TIME (enum): 16:20
                LONG_TIME (enum): 16:20:30
                SHORT_DATE (enum): 20/04/2021
                LONG_DATE (enum): 20 April 2021
                DEFAULT (enum): 20 April 2021 16:20
                LONG_DATE_TIME (enum): Tuesday, 20 April 2021 16:20
                RELATIVE_TIME (enum): 2 months ago
            '''
            SHORT_TIME = 't'
            LONG_TIME = 'T'
            SHORT_DATE = 'd'
            LONG_DATE = 'D'
            DEFAULT = 'f'
            LONG_DATE_TIME = 'F'
            RELATIVE_TIME = 'R'

        @classmethod
        def timestamp(cls, timestamp: datetime.datetime = None, flag: Union[TIMESTAMP_FLAGS, str] = TIMESTAMP_FLAGS.DEFAULT) -> str:
            '''Return valid timestamp string. Discord will display this in a useful way.

            Arguments:
                timestamp (datetime): The timestamp to parse, can be omitted to use `now`.
                flag (TIMESTAMP_FLAGS|str): Flag to use when parsing the timestamp on the client.

            Returns:
                str: Valid string to use as part of a discord message to reference to a point in time.
            '''
            if timestamp is None:
                timestamp = datetime.datetime.now()
            if type(flag) is cls.TIMESTAMP_FLAGS:
                flag = flag.value
            return f'<t:{int(timestamp.timestamp())}:{flag}>'

        @classmethod
        def user(cls, user: 'Union[snowflake.Snowflake, ext_user.User, ext_user.Member]'):
            '''Return valid mention string for the user's name.

            Arguments:
                user (Snowflake|User|Member): User or User's ID to mention.

            Returns:
                str: Valid string to use as part of a discord message to reference a User by name.
            '''
            if isinstance(user, (snowflake.Snowflake, str)):
                user_id = user
            elif isinstance(user, (ext_user.User, ext_user.Member)):
                user_id = user.id
            return f'<@{user_id}>'

        @classmethod
        def user_nickname(cls, user: 'Union[snowflake.Snowflake, ext_user.User, ext_user.Member]'):
            '''Return valid mention string for the user's nickname.

            Arguments:
                user (Snowflake|User|Member): User or User's ID to mention.

            Returns:
                str: Valid string to use as part of a discord message to reference a User by nickname.
            '''
            if isinstance(user, (snowflake.Snowflake, str)):
                user_id = user
            elif isinstance(user, (ext_user.User, ext_user.Member)):
                user_id = user.id
            return f'<@!{user_id}>'

        @classmethod
        def channel(cls, channel: 'Union[snowflake.Snowflake, ext_channel.Channel]'):
            '''Return valid mention string for the channel.

            Arguments:
                channel (Snowflake|Channel): Channel or channel ID to mention. Any subclass of Channel is accepted.

            Returns:
                str: Valid string to use as part of a discord message to reference a Channel.
            '''
            if isinstance(channel, (snowflake.Snowflake, str)):
                channel_id = channel
            elif isinstance(channel, ext_channel.Channel):
                channel_id = channel.id
            return f'<#{channel_id}>'

        @classmethod
        def role(cls, role: 'Union[snowflake.Snowflake, ext_role.Role]'):
            '''Return valid mention string for the role.

            Arguments:
                role (Snowflake|Role): Role or role's ID to mention.

            Returns:
                str: Valid string to use as part of a discord message to reference a Role.
            '''
            if isinstance(role, (snowflake.Snowflake, str)):
                role_id = role
            elif isinstance(role, ext_role.Role):
                role_id = role.id
            return f'<@&{role_id}>'


class MessageReference(BaseDiscordObject):
    '''Slim data holding class.

    Attributes:
        message_id (Snowflake|None): ID of the originating message.
        channel_id: (Snowflake|None): ID of the originating message's channel.
        guild_id: (Snowflake|None): ID of the originating message's guild.
        fail_if_not_exists (bool|None): When sending, whether to error if the referenced message doesn't exist instead of sending as a normal (non-reply) message, default true

    '''

    message_id: Optional[snowflake.Snowflake] = None  # id of the originating message
    channel_id: Optional[snowflake.Snowflake] = None  # id of the originating message's channel
    guild_id: Optional[snowflake.Snowflake] = None  # id of the originating message's guild
    fail_if_not_exists: Optional[bool] = None  # when sending, whether to error if the referenced message doesn't exist instead of sending as a normal (non-reply) message, default true

    def from_dict(self, data: dict) -> 'MessageReference':
        '''Parse a MessageReference from an API compliant dict.'''
        if 'message_id' in data:
            self.message_id = snowflake.Snowflake(data['message_id'])
        if 'channel_id' in data:
            self.channel_id = snowflake.Snowflake(data['channel_id'])
        if 'guild_id' in data:
            self.guild_id = snowflake.Snowflake(data['guild_id'])
        if 'fail_if_not_exists' in data:
            self.fail_if_not_exists = data['fail_if_not_exists']

        return self
