import enum
from typing import Optional, List

from .base_object import BaseDiscordObject

from . import snowflake, channel as ext_channel


class Guild(BaseDiscordObject):
    '''Commonly know as a server.'''

    class VerificationLevels(enum.IntEnum):
        '''Level of verification required by the guild.

        TODO: Move this to enumerations.
        '''
        NONE = 0  # unrestricted
        LOW = 1  # must have verified email on account
        MEDIUM = 2  # must be registered on Discord for longer than 5 minutes
        HIGH = 3  # must be a member of the server for longer than 10 minutes
        VERY_HIGH = 4  # must have a verified phone number

    class NSFWLevels(enum.IntEnum):
        '''NSFW level allowed in guild.

        TODO: Move this to enumerations.
        '''
        DEFAULT = 0
        EXPLICIT = 1
        SAFE = 2
        AGE_RESTRICTED = 3

    class PremiumTiers(enum.IntEnum):
        '''Premium tier currently unlocked by guild.

        TODO: Move this to enumerations.
        '''
        NONE = 0  # guild has not unlocked any Server Boost perks
        TIER_1 = 1  # guild has unlocked Server Boost level 1 perks
        TIER_2 = 2  # guild has unlocked Server Boost level 2 perks
        TIER_3 = 3  # guild has unlocked Server Boost level 3 perks

    class FeatureFlags(enum.Flag):
        '''Features of guild.

        TODO: Move this to enumerations.
        '''
        ANIMATED_ICON = enum.auto()  # guild has access to set an animated guild icon
        BANNER = enum.auto()  # guild has access to set a guild banner image
        COMMERCE = enum.auto()  # guild has access to use commerce features (i.e. create store channels)
        COMMUNITY = enum.auto()  # guild can enable welcome screen, Membership Screening, stage channels and discovery, and receives community updates
        DISCOVERABLE = enum.auto()  # guild is able to be discovered in the directory
        FEATURABLE = enum.auto()  # guild is able to be featured in the directory
        INVITE_SPLASH = enum.auto()  # guild has access to set an invite splash background
        MEMBER_VERIFICATION_GATE_ENABLED = enum.auto()  # guild has enabled Membership Screening
        NEWS = enum.auto()  # guild has access to create news channels
        PARTNERED = enum.auto()  # guild is partnered
        PREVIEW_ENABLED = enum.auto()  # guild can be previewed before joining via Membership Screening or the directory
        VANITY_URL = enum.auto()  # guild has access to set a vanity URL
        VERIFIED = enum.auto()  # guild is verified
        VIP_REGIONS = enum.auto()  # guild has access to set 384kbps bitrate in voice (previously VIP voice servers)
        WELCOME_SCREEN_ENABLED = enum.auto()  # guild has enabled the welcome screen
        TICKETED_EVENTS_ENABLED = enum.auto()  # guild has enabled ticketed events
        MONETIZATION_ENABLED = enum.auto()  # guild has enabled monetization
        MORE_STICKERS = enum.auto()  # guild has increased custom sticker slots
        THREE_DAY_THREAD_ARCHIVE = enum.auto()  # guild has access to the three day archive time for threads
        SEVEN_DAY_THREAD_ARCHIVE = enum.auto()  # guild has access to the seven day archive time for threads
        PRIVATE_THREADS = enum.auto()  # guild has access to create private threads

    id: snowflake.Snowflake = None  # type: ignore
    name: str = None  # type: ignore
    icon: str = None  # type: ignore
    icon_hash: Optional[str] = None  # type: ignore
    splash: Optional[str] = None  # type: ignore
    discovery_splash: Optional[str] = None  # type: ignore

    am_owner: bool = None  # type: ignore # boolean true if the user is the owner of the guild
    owner_id: Optional['snowflake.Snowflake'] = None  # type: ignore # snowflake id of owner
    permissions: type = None  # type: ignore # string total permissions for the user in the guild (excludes overwrites)
    region: type = None  # type: ignore # string voice region id for the guild (deprecated)
    afk_channel_id: type = None  # type: ignore # snowflake id of afk channel
    afk_timeout: type = None  # type: ignore # integer afk timeout in seconds
    widget_enabled: type = None  # type: ignore # boolean true if the server widget is enabled
    widget_channel_id: type = None  # type: ignore # snowflake the channel id that the widget will generate an invite to, or null if set to no invite
    verification_level: type = None  # type: ignore # integer verification level required for the guild
    default_message_notifications: type = None  # type: ignore # integer default message notifications level
    explicit_content_filter: type = None  # type: ignore # integer explicit content filter level
    roles: type = None  # type: ignore # array of role objects roles in the guild
    emojis: type = None  # type: ignore # array of emoji objects custom guild emojis
    features: type = None  # type: ignore # array of guild feature strings enabled guild features
    mfa_level: type = None  # type: ignore # integer required MFA level for the guild
    application_id: type = None  # type: ignore # snowflake application id of the guild creator if it is bot-created
    system_channel_id: type = None  # type: ignore # snowflake the id of the channel where guild notices such as welcome messages and boost events are posted
    system_channel_flags: type = None  # type: ignore # integer system channel flags
    rules_channel_id: type = None  # type: ignore # snowflake the id of the channel where Community guilds can display rules and/or guidelines
    joined_at: type = None  # type: ignore # * ISO8601 timestamp when this guild was joined at
    large: type = None  # type: ignore # * boolean true if this is considered a large guild
    unavailable: type = None  # type: ignore # * boolean true if this guild is unavailable due to an outage
    member_count: type = None  # type: ignore # * integer total number of members in this guild
    voice_states: type = None  # type: ignore # * array of partial voice state objects states of members currently in voice channels; lacks the guild_id key
    members: type = None  # type: ignore # * array of guild member objects users in the guild
    channels: List['ext_channel.Channel'] = None  # type: ignore # * array of channel objects channels in the guild
    threads: type = None  # type: ignore # * array of channel objects all active threads in the guild that current user has permission to view
    presences: type = None  # type: ignore # * array of partial presence update objects presences of the members in the guild,
    #  will only include non-offline members if the size is greater than large threshold
    max_presences: type = None  # type: ignore # integer the maximum number of presences for the guild (null is always returned, apart from the largest of guilds)
    max_members: type = None  # type: ignore # integer the maximum number of members for the guild
    vanity_url_code: type = None  # type: ignore # string the vanity url code for the guild
    description: type = None  # type: ignore # string the description of a Community guild
    banner: type = None  # type: ignore # string banner hash
    premium_tier: type = None  # type: ignore # integer premium tier (Server Boost level)
    premium_subscription_count: type = None  # type: ignore # integer the number of boosts this guild currently has
    preferred_locale: type = None  # type: ignore # string the preferred locale of a Community guild; used in server discovery and notices from Discord; defaults to "en-US"
    public_updates_channel_id: type = None  # type: ignore # snowflake the id of the channel where admins and moderators of Community guilds receive notices from Discord
    max_video_channel_users: type = None  # type: ignore # integer the maximum amount of users in a video channel
    approximate_member_count: type = None  # type: ignore # integer approximate number of members in this guild, returned from the GET /guilds/<id> endpoint when with_counts is true
    approximate_presence_count: type = None  # type: ignore # integer approximate number of non-offline members in this guild, returned from the GET /guilds/<id> endpoint when with_counts is true
    welcome_screen: type = None  # type: ignore # welcome screen object the welcome screen of a Community guild, shown to new members, returned in an Invite's guild object
    nsfw_level: type = None  # type: ignore # integer guild NSFW level
    stage_instances: type = None  # type: ignore # * array of stage instance objects Stage instances in the guild
    stickers: type = None  # type: ignore # array of sticker objects custom guild stickers

    def __str__(self):
        '''Return string representation.'''
        fields = []

        if self.id is not None:
            fields.append(f'id={self.id}')

        if self.name is not None:
            fields.append(f'name={self.name}')

        return f'Guild({", ".join(fields)})'

    def __repr__(self):
        '''Return string representation.'''
        return self.__str__()

    def from_dict(self, data: dict) -> 'Guild':
        '''Parse a Guild from an API compliant dict.'''
        self.id = snowflake.Snowflake(data.get('id'))
        self.name = data['name']
        self.icon = data['icon']
        self.icon_hash = data.get('icon_hash', None)
        self.splash = data.get('splash', None)
        self.afk_channel_id = data.get('afk_channel_id', None)
        self.verification_level = data.get('verification_level', None)
        self.discovery_splash = data.get('discovery_splash', None)
        if 'owner' in data:
            self.am_owner = data['owner']
        if 'owner_id' in data:
            self.owner_id = snowflake.Snowflake(data['owner_id'])

        self.approximate_member_count = data.get('approximate_member_count', None)
        self.approximate_presence_count = data.get('approximate_presence_count', None)

        self.channels = []
        # Process in channels
        if 'channels' in data:
            for channel_dict in data['channels']:
                # Generate channel
                new_channel = ext_channel.ChannelImporter.from_dict(channel_dict, self)
                self.channels.append(new_channel)

        return self
