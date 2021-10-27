
import enum


class INTENTS(enum.IntFlag):
    '''Intents of the user.'''

    GUILDS = (1 << 0)
    # GUILD_CREATE = (1 << 0)
    # GUILD_UPDATE = (1 << 0)
    # GUILD_DELETE = (1 << 0)
    # GUILD_ROLE_CREATE = (1 << 0)
    # GUILD_ROLE_UPDATE = (1 << 0)
    # GUILD_ROLE_DELETE = (1 << 0)
    # CHANNEL_CREATE = (1 << 0)
    # CHANNEL_UPDATE = (1 << 0)
    # CHANNEL_DELETE = (1 << 0)
    # CHANNEL_PINS_UPDATE = (1 << 0)
    # THREAD_CREATE = (1 << 0)
    # THREAD_UPDATE = (1 << 0)
    # THREAD_DELETE = (1 << 0)
    # THREAD_LIST_SYNC = (1 << 0)
    # THREAD_MEMBER_UPDATE = (1 << 0)
    # THREAD_MEMBERS_UPDATE = (1 << 0)
    # STAGE_INSTANCE_CREATE = (1 << 0)
    # STAGE_INSTANCE_UPDATE = (1 << 0)
    # STAGE_INSTANCE_DELETE = (1 << 0)

    GUILD_MEMBERS = (1 << 1)
    # GUILD_MEMBER_ADD = (1 << 1)
    # GUILD_MEMBER_UPDATE = (1 << 1)
    # GUILD_MEMBER_REMOVE = (1 << 1)
    # THREAD_MEMBERS_UPDATE = (1 << 1)

    GUILD_BANS = (1 << 2)
    # GUILD_BAN_ADD = (1 << 2)
    # GUILD_BAN_REMOVE = (1 << 2)

    GUILD_EMOJIS_AND_STICKERS = (1 << 3)
    # GUILD_EMOJIS_UPDATE = (1 << 3)
    # GUILD_STICKERS_UPDATE = (1 << 3)

    GUILD_INTEGRATIONS = (1 << 4)
    # GUILD_INTEGRATIONS_UPDATE = (1 << 4)
    # INTEGRATION_CREATE = (1 << 4)
    # INTEGRATION_UPDATE = (1 << 4)
    # INTEGRATION_DELETE = (1 << 4)

    GUILD_WEBHOOKS = (1 << 5)
    # WEBHOOKS_UPDATE = (1 << 5)

    GUILD_INVITES = (1 << 6)
    # INVITE_CREATE = (1 << 6)
    # INVITE_DELETE = (1 << 6)

    GUILD_VOICE_STATES = (1 << 7)
    # VOICE_STATE_UPDATE = (1 << 7)

    GUILD_PRESENCES = (1 << 8)
    # PRESENCE_UPDATE = (1 << 8)

    GUILD_MESSAGES = (1 << 9)
    # MESSAGE_CREATE = (1 << 9)
    # MESSAGE_UPDATE = (1 << 9)
    # MESSAGE_DELETE = (1 << 9)
    # MESSAGE_DELETE_BULK = (1 << 9)

    GUILD_MESSAGE_REACTIONS = (1 << 10)
    # MESSAGE_REACTION_ADD = (1 << 10)
    # MESSAGE_REACTION_REMOVE = (1 << 10)
    # MESSAGE_REACTION_REMOVE_ALL = (1 << 10)
    # MESSAGE_REACTION_REMOVE_EMOJI = (1 << 10)

    GUILD_MESSAGE_TYPING = (1 << 11)
    # TYPING_START = (1 << 11)

    DIRECT_MESSAGES = (1 << 12)
    # MESSAGE_CREATE = (1 << 12)
    # MESSAGE_UPDATE = (1 << 12)
    # MESSAGE_DELETE = (1 << 12)
    # CHANNEL_PINS_UPDATE = (1 << 12)

    DIRECT_MESSAGE_REACTIONS = (1 << 13)
    # MESSAGE_REACTION_ADD = (1 << 13)
    # MESSAGE_REACTION_REMOVE = (1 << 13)
    # MESSAGE_REACTION_REMOVE_ALL = (1 << 13)
    # MESSAGE_REACTION_REMOVE_EMOJI = (1 << 13)

    DIRECT_MESSAGE_TYPING = (1 << 14)
    # TYPING_START = (1 << 14)


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
