import enum
import datetime
from typing import List

from . import snowflake, role
from .base_object import BaseDiscordObject
from .. import utilities


class User(BaseDiscordObject):

    @enum.unique
    class UserFlag(enum.IntFlag):
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
        NONE = 0
        NITRO_CLASSIC = 1 << 0
        NITRO = 1 << 1

    id: snowflake.Snowflake
    username: str
    discriminator: str
    avatar: str
    bot: bool
    system: bool
    mfa_enabled: bool
    banner: str
    accent_color: int  # TODO: This is actually a color object!
    locale: str
    verified: bool
    email: str
    flags: int
    premium_type: int
    public_flags: int

    def __str__(self):
        fields = []

        if 'id' in self.__dict__:
            fields.append(f'id={self.id}')

        if ('username' in self.__dict__) and ('discriminator' in self.__dict__):
            fields.append(f'username=\'{self.username}#{self.discriminator}\'')

        return f'User({", ".join(fields)})'

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id

    # TODO: We could have a lot of handy "is_X" functions here to return if user is something form the USER_FLAG enumeration

    @property
    def mention(self):
        return f'<@{self.id}>'

    @property
    def mention_nickname(self):
        return f'<@!{self.id}>'

    def ingest_raw_dict(self, data: dict) -> 'User':
        '''
        Ingest and cache a given object for future use.
        '''
        self.from_dict(data)

        self.cache()

        return self

    def from_dict(self, data: dict) -> 'User':
        # Required fields
        self.id = snowflake.Snowflake(data['id'])
        self.username = data['username']
        self.discriminator = data['discriminator']
        self.avatar = data['avatar']

        # Optional fields
        if 'bot' in data:
            self.bot = data['bot']
        if 'system' in data:
            self.system = data['system']

        return self

    def cache(self):
        utilities.Cache().add(self)


class Member(User):
    nick: str
    avatar: str
    roles: List[role.Role]
    joined_at: datetime.datetime
    premium_since: datetime.datetime
    deaf: bool
    mute: bool
    pending: bool
    permissions: str

    def __str__(self):
        fields = []

        if hasattr(self, 'id'):
            fields.append(f'id={self.id}')

        if hasattr(self, 'username') and hasattr(self, 'discriminator'):
            fields.append(f'username=\'{self.username}#{self.discriminator}\'')

        if hasattr(self, 'nick'):
            fields.append(f'nick=\'{self.nick}\'')

        return f'Member({", ".join(fields)})'

    def from_dict(self, data: dict) -> 'Member':
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
        return self

    def update_from_user(self, user: User) -> 'Member':  # noqa: C901
        if hasattr(user, 'id'):
            self.id = user.id
        if hasattr(user, 'username'):
            self.username = user.username
        if hasattr(user, 'discriminator'):
            self.discriminator = user.discriminator
        if hasattr(user, 'avatar'):
            self.avatar = user.avatar
        if hasattr(user, 'bot'):
            self.bot = user.bot
        if hasattr(user, 'system'):
            self.system = user.system
        if hasattr(user, 'mfa_enabled'):
            self.mfa_enabled = user.mfa_enabled
        if hasattr(user, 'banner'):
            self.banner = user.banner
        if hasattr(user, 'accent_color'):
            self.accent_color = user.accent_color
        if hasattr(user, 'locale'):
            self.locale = user.locale
        if hasattr(user, 'verified'):
            self.verified = user.verified
        if hasattr(user, 'email'):
            self.email = user.email
        if hasattr(user, 'flags'):
            self.flags = user.flags
        if hasattr(user, 'premium_type'):
            self.premium_type = user.premium_type
        if hasattr(user, 'public_flags'):
            self.public_flags = user.public_flags
        return self

    def ingest_raw_dict(self, data: dict) -> 'User':
        '''
        Ingest and cache a given object for future use.
        '''
        self.from_dict(data)

        self.cache()

        return self

    def cache(self):
        utilities.Cache().add(self)
