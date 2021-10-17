import enum


class DISCORD_EVENTS(enum.Enum):
    '''Enumeration of various discord events.

    Attributes:
        CHANNEL_CREATE (enum):
        CHANNEL_DELETE (enum):
        CHANNEL_PINS_UPDATE (enum):
        CHANNEL_UPDATE (enum):
        GUILD_BAN_ADD (enum):
        GUILD_BAN_REMOVE (enum):
        GUILD_CREATE (enum):
        GUILD_DELETE (enum):
        GUILD_EMOJIS_UPDATE (enum):
        GUILD_INTEGRATIONS_UPDATE (enum):
        GUILD_MEMBER_ADD (enum):
        GUILD_MEMBER_REMOVE (enum):
        GUILD_MEMBER_UPDATE (enum):
        GUILD_ROLE_CREATE (enum):
        GUILD_ROLE_DELETE (enum):
        GUILD_ROLE_UPDATE (enum):
        GUILD_STICKERS_UPDATE (enum):
        GUILD_UPDATE (enum):
        INTEGRATION_CREATE (enum):
        INTEGRATION_DELETE (enum):
        INTEGRATION_UPDATE (enum):
        INVITE_CREATE (enum):
        INVITE_DELETE (enum):
        MESSAGE_CREATE (enum):
        MESSAGE_DELETE (enum):
        MESSAGE_DELETE_BULK (enum):
        MESSAGE_REACTION_ADD (enum):
        MESSAGE_REACTION_REMOVE (enum):
        MESSAGE_REACTION_REMOVE_ALL (enum):
        MESSAGE_REACTION_REMOVE_EMOJI (enum):
        MESSAGE_UPDATE (enum):
        PRESENCE_UPDATE (enum):
        READY (enum):
        STAGE_INSTANCE_CREATE (enum):
        STAGE_INSTANCE_DELETE (enum):
        STAGE_INSTANCE_UPDATE (enum):
        THREAD_CREATE (enum):
        THREAD_DELETE (enum):
        THREAD_LIST_SYNC (enum):
        THREAD_MEMBER_UPDATE (enum):
        THREAD_MEMBERS_UPDATE (enum):
        THREAD_UPDATE (enum):
        TYPING_START (enum):
        VOICE_STATE_UPDATE (enum):
        WEBHOOKS_UPDATE (enum):
        INTERACTION_CREATE (enum):
    '''
    CHANNEL_CREATE = enum.auto()
    CHANNEL_DELETE = enum.auto()
    CHANNEL_PINS_UPDATE = enum.auto()
    CHANNEL_UPDATE = enum.auto()
    GUILD_BAN_ADD = enum.auto()
    GUILD_BAN_REMOVE = enum.auto()
    GUILD_CREATE = enum.auto()
    GUILD_DELETE = enum.auto()
    GUILD_EMOJIS_UPDATE = enum.auto()
    GUILD_INTEGRATIONS_UPDATE = enum.auto()
    GUILD_MEMBER_ADD = enum.auto()
    GUILD_MEMBER_REMOVE = enum.auto()
    GUILD_MEMBER_UPDATE = enum.auto()
    GUILD_ROLE_CREATE = enum.auto()
    GUILD_ROLE_DELETE = enum.auto()
    GUILD_ROLE_UPDATE = enum.auto()
    GUILD_STICKERS_UPDATE = enum.auto()
    GUILD_UPDATE = enum.auto()
    INTEGRATION_CREATE = enum.auto()
    INTEGRATION_DELETE = enum.auto()
    INTEGRATION_UPDATE = enum.auto()
    INVITE_CREATE = enum.auto()
    INVITE_DELETE = enum.auto()
    MESSAGE_CREATE = enum.auto()
    MESSAGE_DELETE = enum.auto()
    MESSAGE_DELETE_BULK = enum.auto()
    MESSAGE_REACTION_ADD = enum.auto()
    MESSAGE_REACTION_REMOVE = enum.auto()
    MESSAGE_REACTION_REMOVE_ALL = enum.auto()
    MESSAGE_REACTION_REMOVE_EMOJI = enum.auto()
    MESSAGE_UPDATE = enum.auto()
    PRESENCE_UPDATE = enum.auto()
    READY = enum.auto()
    STAGE_INSTANCE_CREATE = enum.auto()
    STAGE_INSTANCE_DELETE = enum.auto()
    STAGE_INSTANCE_UPDATE = enum.auto()
    THREAD_CREATE = enum.auto()
    THREAD_DELETE = enum.auto()
    THREAD_LIST_SYNC = enum.auto()
    THREAD_MEMBER_UPDATE = enum.auto()
    THREAD_MEMBERS_UPDATE = enum.auto()
    THREAD_UPDATE = enum.auto()
    TYPING_START = enum.auto()
    VOICE_STATE_UPDATE = enum.auto()
    WEBHOOKS_UPDATE = enum.auto()
    INTERACTION_CREATE = enum.auto()


class MESSAGE_TYPE(enum.IntEnum):
    '''Types of messages.'''
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


class CHANNEL_TYPES(enum.IntEnum):
    '''Types of channels.'''
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


class EMBED_TYPES(enum.Enum):
    '''Types of Embeds.'''
    rich = enum.auto()      # generic embed rendered from embed attributes
    image = enum.auto()     # image embed
    video = enum.auto()     # video embed
    gifv = enum.auto()      # animated gif image embed rendered as a video embed
    article = enum.auto()   # article embed
    link = enum.auto()      # link embed
