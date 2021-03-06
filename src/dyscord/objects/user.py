import enum
import datetime
from typing import List

from . import snowflake, role
from .base_object import BaseDiscordObject


class User(BaseDiscordObject):
    '''Discord User.

    Attributes:
        id (Snowflake): Unique ID of User. Is a [Snowflake][dyscord.objects.snowflake.Snowflake].
        username (str): Global name of the User.
        discriminator (int): Random set of 4 numbers to discriminate user from others.
        avatar (str): TODO: Look this up.
        bot (bool): User is a bot or not.
    '''

    @enum.unique
    class UserFlag(enum.IntFlag):
        '''Flags on a User.'''
        NONE = 0
        DISCORD_EMPLOYEE = 1 << 0
        PARTNERED_SERVER_OWNER = 1 << 1
        HYPESQUAD_EVENTS = 1 << 2
        BUG_HUNTER_LEVEL_1 = 1 << 3
        HOUSE_BRAVERY = 1 << 6
        HOUSE_BRILLIANCE = 1 << 7
        HOUSE_BALANCE = 1 << 8
        EARLY_SUPPORTER = 1 << 9
        TEAM_USER = 1 << 10
        BUG_HUNTER_LEVEL_2 = 1 << 14
        VERIFIED_BOT = 1 << 16
        EARLY_VERIFIED_BOT_DEVELOPER = 1 << 17
        DISCORD_CERTIFIED_MODERATOR = 1 << 18

    @enum.unique
    class PremiumType(enum.IntFlag):
        '''Type of Premium subscription the User has.'''
        NONE = 0
        NITRO_CLASSIC = 1 << 0
        NITRO = 1 << 1

    id: snowflake.Snowflake = None  # type: ignore
    username: str = None  # type: ignore
    discriminator: str = None  # type: ignore
    avatar: str = None  # type: ignore
    bot: bool = None  # type: ignore
    system: bool = None  # type: ignore
    mfa_enabled: bool = None  # type: ignore
    banner: str = None  # type: ignore
    accent_color: int = None  # type: ignore
    locale: str = None  # type: ignore
    verified: bool = None  # type: ignore
    email: str = None  # type: ignore
    flags: int = None  # type: ignore
    premium_type: int = None  # type: ignore
    public_flags: int = None  # type: ignore

    def __str__(self):
        '''Return a discord compatible mention string.'''
        return self.mention_nickname

    def __repr__(self):
        '''Return a discord compatible mention string.'''
        return self.__str__()

    def __eq__(self, other):
        '''Determine if other User and self are the same User.'''
        if not isinstance(other, User):
            raise NotImplementedError(f'Cannot compare User to [{type(other)}].')
        return self.id == other.id

    # TODO: We could have a lot of handy "is_X" functions here to return if user is something form the USER_FLAG enumeration

    @property
    def mention(self):
        '''Generate a valid name mention for use in Discord.'''
        return f'<@{self.id}>'

    @property
    def mention_nickname(self):
        '''Generate a valid nickname mention for use in Discord.'''
        return f'<@!{self.id}>'

    def from_dict(self, data: dict) -> 'User':  # noqa: C901
        '''Parse a User from an API compliant dict.'''
        # Required fields
        self.id = snowflake.Snowflake(data['id'])

        if 'username' in data:
            self.username = data['username']
        if 'discriminator' in data:
            self.discriminator = data['discriminator']
        if 'avatar' in data:
            self.avatar = data['avatar']

        # Optional fields
        if 'bot' in data:
            self.bot = data['bot']
        if 'system' in data:
            self.system = data['system']
        if 'verified' in data:
            self.verified = data['verified']
        if 'email' in data:
            self.email = data['email']
        if 'banner' in data:
            self.banner = data['banner']
        if 'accent_color' in data:
            self.accent_color = data['accent_color']
        if 'flags' in data:
            self.flags = data['flags']
        if 'premium_type' in data:
            self.premium_type = data['premium_type']
        if 'public_flags' in data:
            self.public_flags = data['public_flags']
        return self


class Member(User):
    '''User within a guild.'''

    nick: str = None  # type: ignore
    avatar: str = None  # type: ignore
    roles: List[role.Role] = None  # type: ignore
    joined_at: datetime.datetime = None  # type: ignore
    premium_since: datetime.datetime = None  # type: ignore
    deaf: bool = None  # type: ignore
    mute: bool = None  # type: ignore
    pending: bool = None  # type: ignore
    permissions: str = None  # type: ignore

    def from_dict(self, data: dict) -> 'Member':
        '''Parse a Member from an API compliant dict.'''
        if 'nick' in data:
            self.nick = data['nick']
        if 'avatar' in data:
            self.avatar = data['avatar']
        if 'joined_at' in data:
            self.joined_at = datetime.datetime.fromisoformat(data['joined_at'])
        if 'premium_since' in data and data['premium_since'] is not None:
            self.premium_since = datetime.datetime.fromisoformat(data['premium_since'])
        if 'deaf' in data:
            self.deaf = data['deaf']
        if 'mute' in data:
            self.mute = data['mute']
        if 'pending' in data:
            self.pending = data['pending']
        if 'permissions' in data:
            self.permissions = data['permissions']
        if 'user' in data:
            tmp_user = User().from_dict(data['user'])
            self.update_from_user(tmp_user)
        return self

    def update_from_user(self, user: User) -> 'Member':  # noqa: C901
        '''Update Member properties from associated user.'''
        if user.id is not None:
            self.id = user.id
        if user.username is not None:
            self.username = user.username
        if user.discriminator is not None:
            self.discriminator = user.discriminator
        if user.avatar is not None:
            self.avatar = user.avatar
        if user.bot is not None:
            self.bot = user.bot
        if user.system is not None:
            self.system = user.system
        if user.mfa_enabled is not None:
            self.mfa_enabled = user.mfa_enabled
        if user.banner is not None:
            self.banner = user.banner
        if user.accent_color is not None:
            self.accent_color = user.accent_color
        if user.locale is not None:
            self.locale = user.locale
        if user.verified is not None:
            self.verified = user.verified
        if user.email is not None:
            self.email = user.email
        if user.flags is not None:
            self.flags = user.flags
        if user.premium_type is not None:
            self.premium_type = user.premium_type
        if user.public_flags is not None:
            self.public_flags = user.public_flags
        return self
