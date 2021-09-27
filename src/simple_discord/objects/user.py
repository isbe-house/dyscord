import enum

from . import snowflake
from .base_object import BaseDiscordObject


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

    def __init__(self):
        self.id: snowflake.Snowflake
        self.username: str
        self.discriminator: str
        self.avatar: str
        self.bot: bool
        self.system: bool
        self.mfa_enabled: bool
        self.banner: str
        self.accent_color: int  # TODO: This is actually a color object!
        self.locale: str
        self.verified: bool
        self.email: str
        self.flags: int
        self.premium_type: int
        self.public_flags: int

    def __str__(self):
        fields = []

        if 'id' in self.__dict__:
            fields.append(f'id={self.id}')

        if ('username' in self.__dict__) and ('discriminator' in self.__dict__):
            fields.append(f'username={self.username}#{self.discriminator}')

        return f'User({",".join(fields)})'

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

        # TODO: Cache users as well.

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
