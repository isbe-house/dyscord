
import enum


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
    '''Types of interactions.

    Attributes:
        PING: Used by server to get online status of webhook based applications. Handled by Dyscord in background.
        APPLICATION_COMMAND: Command was a `/slash` style command, typed by the user.
        MESSAGE_COMPONENT: Command was an interaction directly with a `Message` or `User`, the client right clicked on them.
        APPLICATION_COMMAND_AUTOCOMPLETE: User it attempting to complete an interaction as is asking for suggestions.
    '''
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4


class INTERACTION_RESPONSE_TYPES(enum.IntEnum):
    '''Types of interaction responses.

    Attributes:
        PONG: ACK a Ping.
        CHANNEL_MESSAGE_WITH_SOURCE: Respond to an interaction with a message.
        DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE: ACK an interaction and edit a response later, the user sees a loading state.
        DEFERRED_UPDATE_MESSAGE: Only for components (Not slash commands), ACK an interaction and edit the original message later; the user does not see a loading state.
        UPDATE_MESSAGE: Only for components (Not slash commands), edit the message the component was attached to.
        APPLICATION_COMMAND_AUTOCOMPLETE_RESULT: Respond to an autocomplete interaction with suggested choices.

    '''
    PONG = 1  # ACK a Ping
    CHANNEL_MESSAGE_WITH_SOURCE = 4  # respond to an interaction with a message
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5  # ACK an interaction and edit a response later, the user sees a loading state
    DEFERRED_UPDATE_MESSAGE = 6  # for components, ACK an interaction and edit the original message later; the user does not see a loading state
    UPDATE_MESSAGE = 7  # for components, edit the message the component was attached to
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8  # respond to an autocomplete interaction with suggested choices


class INTERACTION_CALLBACK_FLAGS(enum.IntFlag):
    '''Flags for callback methods.'''
    NONE = 0
    EPHEMERAL = (1 << 6)  # only the user receiving the message can see it
