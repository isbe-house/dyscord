import enum
from typing import Optional, Union


class Permissions:
    '''Permissions for users and roles.'''

    class PermissionFlags(enum.IntFlag):
        '''Various flags that can be set.'''

        CREATE_INSTANT_INVITE = (1 << 0)        # Allows creation of instant invites	T, V, S
        KICK_MEMBERS = (1 << 1)                 # Allows kicking members
        BAN_MEMBERS = (1 << 2)                  # Allows banning members
        ADMINISTRATOR = (1 << 3)                # Allows all permissions and bypasses channel permission overwrites
        MANAGE_CHANNELS = (1 << 4)              # Allows management and editing of channels	T, V, S
        MANAGE_GUILD = (1 << 5)                 # Allows management and editing of the guild
        ADD_REACTIONS = (1 << 6)                # Allows for the addition of reactions to messages	T
        VIEW_AUDIT_LOG = (1 << 7)               # Allows for viewing of audit logs
        PRIORITY_SPEAKER = (1 << 8)             # Allows for using priority speaker in a voice channel	V
        STREAM = (1 << 9)                       # Allows the user to go live	V
        VIEW_CHANNEL = (1 << 10)                # Allows guild members to view a channel, which includes reading messages in text channels	T, V, S
        SEND_MESSAGES = (1 << 11)               # Allows for sending messages in a channel (does not allow sending messages in threads)	T
        SEND_TTS_MESSAGES = (1 << 12)           # Allows for sending of /tts messages	T
        MANAGE_MESSAGES = (1 << 13)             # Allows for deletion of other users messages	T
        EMBED_LINKS = (1 << 14)                 # Links sent by users with this permission will be auto-embedded	T
        ATTACH_FILES = (1 << 15)                # Allows for uploading images and files	T
        READ_MESSAGE_HISTORY = (1 << 16)        # Allows for reading of message history	T
        MENTION_EVERYONE = (1 << 17)            # Allows for using the @everyone tag to notify all users in a channel, and the @here tag to notify all online users in a channel	T
        USE_EXTERNAL_EMOJIS = (1 << 18)         # Allows the usage of custom emojis from other servers	T
        VIEW_GUILD_INSIGHTS = (1 << 19)         # Allows for viewing guild insights
        CONNECT = (1 << 20)                     # Allows for joining of a voice channel	V, S
        SPEAK = (1 << 21)                       # Allows for speaking in a voice channel	V
        MUTE_MEMBERS = (1 << 22)                # Allows for muting members in a voice channel	V, S
        DEAFEN_MEMBERS = (1 << 23)              # Allows for deafening of members in a voice channel	V, S
        MOVE_MEMBERS = (1 << 24)                # Allows for moving of members between voice channels	V, S
        USE_VAD = (1 << 25)                     # Allows for using voice-activity-detection in a voice channel	V
        CHANGE_NICKNAME = (1 << 26)             # Allows for modification of own nickname
        MANAGE_NICKNAMES = (1 << 27)            # Allows for modification of other users nicknames
        MANAGE_ROLES = (1 << 28)                # Allows management and editing of roles	T, V, S
        MANAGE_WEBHOOKS = (1 << 29)             # Allows management and editing of webhooks	T
        MANAGE_EMOJIS_AND_STICKERS = (1 << 30)  # Allows management and editing of emojis and stickers
        USE_APPLICATION_COMMANDS = (1 << 31)    # Allows members to use application commands, including slash commands and context menu commands.	T
        REQUEST_TO_SPEAK = (1 << 32)            # Allows for requesting to speak in stage channels. (This permission is under active development and may be changed or removed.)	S
        MANAGE_THREADS = (1 << 34)              # Allows for deleting and archiving threads, and viewing all private threads	T
        CREATE_PUBLIC_THREADS = (1 << 35)       # Allows for creating threads	T
        CREATE_PRIVATE_THREADS = (1 << 36)      # Allows for creating private threads	T
        USE_EXTERNAL_STICKERS = (1 << 37)       # Allows the usage of custom stickers from other servers	T
        SEND_MESSAGES_IN_THREADS = (1 << 38)    # Allows for sending messages in threads	T
        START_EMBEDDED_ACTIVITIES = (1 << 39)   # Allows for launching activities (applications with the EMBEDDED flag) in a voice channel	V

    def __init__(self, data: Optional[Union[int, str, 'Permissions']] = None):
        '''Init.'''
        self.permissions: set

        if type(data) in [str, int]:
            self.parse_str(str(data))
        elif type(data) is Permissions:
            self.permissions = data.permissions
        elif data is None:
            self.permissions = set()
        else:
            raise TypeError(f'Cannot parse in a {type(data)}!')

    def set(self, flag):
        '''Set a specific flag.'''

    def clear(self, flag):
        '''Clear a specific flag.'''

    def parse_str(self, data):
        '''Parse a string as a permission.'''
        data = int(data)
        self.permissions = set()
        for permission in self.PermissionFlags:
            if permission & data:
                self.permissions.add(permission)

    def __and__(self, other):
        '''Logically AND two Permissions together.'''
        if type(other) is Permissions:
            new_permissions = Permissions()

            for permission in other.permissions:
                if permission in self.permissions:
                    new_permissions.set(permission)
            for permission in self.permissions:
                if permission in other.permissions:
                    new_permissions.set(permission)
            return new_permissions

        elif type(other) is self.PermissionFlags:
            return other in self.permissions

        elif type(other) in [int, str]:
            if type(other) is str:
                other = int(other)

        raise TypeError(f'Cannot AND a Permission against a {type(other)}!')

    def __rand__(self, other):
        '''See __and__().'''
        return self.__and__(other)

    def __eq__(self, other):
        '''Determine if two permission objects are equivalent.'''
        assert type(other) is Permissions
        return self.permissions == other.permissions
