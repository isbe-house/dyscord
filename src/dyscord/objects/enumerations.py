import enum


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
