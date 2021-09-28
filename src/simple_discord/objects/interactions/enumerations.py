
import enum


class CHANNEL_TYPE(enum.IntEnum):
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
    CHAT_INPUT = 1  # Slash commands; a text-based command that shows up when a user types /
    USER = 2  # A UI-based command that shows up when you right click or tap on a user
    MESSAGE = 3  # A UI-based command that shows up when you right click or tap on a message


class COMMAND_OPTION(enum.IntEnum):
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
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3


class BUTTON_STYLES(enum.IntEnum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5
