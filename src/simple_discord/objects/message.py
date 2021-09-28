import datetime
import enum
from typing import Union, Optional, List, Dict

from .base_object import BaseDiscordObject
from . import user, channel, snowflake
from .interactions import components


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
        self.components: List[components.Component]  # Message components TBD
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

    def to_sendable_dict(self) -> dict:
        '''
        Sending a message only allows a subset of attributes. Ignore anything else about this message when producing that dict.
        '''
        new_dict: Dict[str, object] = dict()
        new_dict['content'] = self.content if hasattr(self, 'content') else None
        # new_dict['tts'] = self.tts if hasattr(self, 'tts') else False
        # new_dict['file'] = None  # TODO: Handle a file upload.
        # new_dict['embeds'] = None  # TODO: Handle embeds.
        # new_dict['allowed_mentions'] = True  # BUG: This isn't a bool, its an `AllowedMentionsObject`, which we don't support yet.
        # new_dict['message_reference'] = None
        # new_dict['sticker_ids'] = None

        if hasattr(self, 'components') and type(self.components) is list and len(self.components):
            new_dict['components'] = list()
            assert type(new_dict['components']) is list
            for component in self.components:
                new_dict['components'].append(component.to_dict())

        return new_dict

    def add_components(self) -> 'components.ActionRow':
        '''
        Start adding components by starting an ACTION_ROW.
        '''
        if not hasattr(self, 'components'):
            self.components = list()
        new_action_row = components.ActionRow()
        self.components.append(new_action_row)

        return new_action_row

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
                assert type(component) is components.ActionRow,\
                    f'Got invalid type {type(component)} in Message.components, must be ActionRow.'
                component.validate()

                if type(component) is components.ActionRow:
                    for sub_component in component.components:
                        if hasattr(sub_component, 'custom_id'):
                            assert sub_component.custom_id not in custom_ids,\
                                f'Found duplicate custom_id [{sub_component.custom_id}]'
                            custom_ids.append(sub_component.custom_id)
                else:
                    if hasattr(component, 'custom_id'):
                        assert component.custom_id not in custom_ids,\
                            f'Found duplicate custom_id [{component.custom_id}]'
                        custom_ids.append(component.custom_id)
