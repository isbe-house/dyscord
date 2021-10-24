
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
