
import enum


class CHANNEL_TYPE(enum.IntEnum):
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


class COMMAND_TYPE(enum.IntEnum):
    '''Type of command.

    Attributes:
        CHAT_INPUT (int): Slash commands; a text-based command that shows up when a user types.
        USER (int): A UI-based command that shows up when you right click or tap on a user.
        MESSAGE (int): A UI-based command that shows up when you right click or tap on a message.
    '''
    CHAT_INPUT = 1  # Slash commands; a text-based command that shows up when a user types
    USER = 2  # A UI-based command that shows up when you right click or tap on a user
    MESSAGE = 3  # A UI-based command that shows up when you right click or tap on a message


class COMMAND_OPTION(enum.IntEnum):
    '''Valid types or groupings of command options.'''
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4  # Any integer between -2^53 and 2^53
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7  # Includes all channel types + categories
    ROLE = 8
    MENTIONABLE = 9  # Includes users and roles
    NUMBER = 10  # Any double between -2^53 and 2^53


class COMPONENT_TYPES(enum.IntEnum):
    '''Types of Components.'''
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3


class BUTTON_STYLES(enum.IntEnum):
    '''Styles of Button objects.'''
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class INTERACTION_TYPES(enum.IntEnum):
    '''Types of interactions.'''
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3


class INTERACTION_RESPONSE_TYPES(enum.IntEnum):
    '''Types of interaction responses.'''
    PONG = 1  # ACK a Ping
    CHANNEL_MESSAGE_WITH_SOURCE = 4  # respond to an interaction with a message
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5  # ACK an interaction and edit a response later, the user sees a loading state
    DEFERRED_UPDATE_MESSAGE = 6  # for components, ACK an interaction and edit the original message later; the user does not see a loading state
    UPDATE_MESSAGE = 7  # for components, edit the message the component was attached to


class INTERACTION_CALLBACK_FLAGS(enum.IntFlag):
    '''Flags for callback methods.'''
    EPHEMERAL = (1 << 6)  # only the user receiving the message can see it
