import datetime
import enum
from typing import Union, Optional

from .base_object import BaseDiscordObject
from . import user, channel, snowflake


class Message(BaseDiscordObject):

    class MessageType(enum.IntEnum):
        DEFAULT = 0
        RECIPIENT_ADD = 1
        RECIPIENT_REMOVE = 2
        CALL = 3
        CHANNEL_NAME_CHANGE = 4
        CHANNEL_ICON_CHANGE = 5
        CHANNEL_PINNED_MESSAGE = 6
        GUILD_MEMBER_JOIN = 7
        USER_PREMIUM_GUILD_SUBSCRIPTION = 8
        USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
        USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
        USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
        CHANNEL_FOLLOW_ADD = 12
        GUILD_DISCOVERY_DISQUALIFIED = 14
        GUILD_DISCOVERY_REQUALIFIED = 15
        GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
        GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
        THREAD_CREATED = 18
        REPLY = 19
        CHAT_INPUT_COMMAND = 20
        THREAD_STARTER_MESSAGE = 21
        GUILD_INVITE_REMINDER = 22
        CONTEXT_MENU_COMMAND = 23

    def __init__(self):
        self.id: snowflake.Snowflake
        self.channel_id: snowflake.Snowflake
        self.guild_id: Optional[snowflake.Snowflake]
        self.author: user.User
        self.member: Optional[user.User]
        self.content: str
        self.timestamp: datetime.datetime
        self.edited_timestamp: Optional[datetime.datetime]
        self.tts: bool
        self.mention_everyone: bool
        self.mentions: list[user.User]
        # self.mention_roles: list[role.Role] = []  # Roles are TBD
        self.mention_channels: list[channel.Channel]
        # self.attachments: list[attachment.Attachment] = []  # Attachments are TBD
        # self.embeds: list[embed.Embed] = []  # Embeds are TBD
        # self.reactions: list[reaction.Reaction] = []  # Reactions are TBD
        self.nonce: Optional[Union[int, str]]
        self.pinned: bool
        self.webhook_id: Optional[snowflake.Snowflake]
        self.type: Message.MessageType
        # self.activity = None  # Activity TBD
        # self.application: application.Application = None  # Application TBD
        self.application_id: snowflake.Snowflake
        # self.message_reference: = None  # Message Reference TBD
        # self.flags = None  # Message Flags TBD
        self.referenced_message: Message
        # self.interaction = None  # Interactions TBD
        self.thread: channel.Channel
        # self.components = None  # Message components TBD
        # self.sticker_items: List[Sticker] = []  # Stickers TBD

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
        self.member = user.User()  # TODO: Update after we can parse in users.
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
        self.type = Message.MessageType(data['type'])

        return self

    def cache(self):
        '''
        Sav object to the cache for faster recall in the future.
        '''
        raise NotImplementedError(f'{__class__.__name__} does not yet implement this function.')
