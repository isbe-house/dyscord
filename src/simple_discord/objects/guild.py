import enum
from typing import Optional, List

from .base_object import BaseDiscordObject

from . import snowflake, channel as ext_channel


class Guild(BaseDiscordObject):

    class VerificationLevels(enum.IntEnum):
        NONE = 0  # unrestricted
        LOW = 1  # must have verified email on account
        MEDIUM = 2  # must be registered on Discord for longer than 5 minutes
        HIGH = 3  # must be a member of the server for longer than 10 minutes
        VERY_HIGH = 4  # must have a verified phone number

    class NSFWLevels(enum.IntEnum):
        DEFAULT = 0
        EXPLICIT = 1
        SAFE = 2
        AGE_RESTRICTED = 3

    class PremiumTiers(enum.IntEnum):
        NONE = 0  # guild has not unlocked any Server Boost perks
        TIER_1 = 1  # guild has unlocked Server Boost level 1 perks
        TIER_2 = 2  # guild has unlocked Server Boost level 2 perks
        TIER_3 = 3  # guild has unlocked Server Boost level 3 perks

    class FeatureFlags(enum.Flag):
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

    id: snowflake.Snowflake
    name: str
    icon: str
    icon_hash: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]

    am_owner: bool  # boolean true if the user is the owner of the guild
    owner_id: Optional['snowflake.Snowflake']  # snowflake id of owner
    permissions: type  # string total permissions for the user in the guild (excludes overwrites)
    region: type  # string voice region id for the guild (deprecated)
    afk_channel_id: type  # snowflake id of afk channel
    afk_timeout: type  # integer afk timeout in seconds
    widget_enabled: type  # boolean true if the server widget is enabled
    widget_channel_id: type  # snowflake the channel id that the widget will generate an invite to, or null if set to no invite
    verification_level: type  # integer verification level required for the guild
    default_message_notifications: type  # integer default message notifications level
    explicit_content_filter: type  # integer explicit content filter level
    roles: type  # array of role objects roles in the guild
    emojis: type  # array of emoji objects custom guild emojis
    features: type  # array of guild feature strings enabled guild features
    mfa_level: type  # integer required MFA level for the guild
    application_id: type  # snowflake application id of the guild creator if it is bot-created
    system_channel_id: type  # snowflake the id of the channel where guild notices such as welcome messages and boost events are posted
    system_channel_flags: type  # integer system channel flags
    rules_channel_id: type  # snowflake the id of the channel where Community guilds can display rules and/or guidelines
    joined_at: type  # * ISO8601 timestamp when this guild was joined at
    large: type  # * boolean true if this is considered a large guild
    unavailable: type  # * boolean true if this guild is unavailable due to an outage
    member_count: type  # * integer total number of members in this guild
    voice_states: type  # * array of partial voice state objects states of members currently in voice channels; lacks the guild_id key
    members: type  # * array of guild member objects users in the guild
    channels: List['ext_channel.Channel']  # * array of channel objects channels in the guild
    threads: type  # * array of channel objects all active threads in the guild that current user has permission to view
    presences: type     # * array of partial presence update objects presences of the members in the guild,
                                        #   will only include non-offline members if the size is greater than large threshold  # noqa: E116
    max_presences: type  # integer the maximum number of presences for the guild (null is always returned, apart from the largest of guilds)
    max_members: type  # integer the maximum number of members for the guild
    vanity_url_code: type  # string the vanity url code for the guild
    description: type  # string the description of a Community guild
    banner: type  # string banner hash
    premium_tier: type  # integer premium tier (Server Boost level)
    premium_subscription_count: type  # integer the number of boosts this guild currently has
    preferred_locale: type  # string the preferred locale of a Community guild; used in server discovery and notices from Discord; defaults to "en-US"
    public_updates_channel_id: type  # snowflake the id of the channel where admins and moderators of Community guilds receive notices from Discord
    max_video_channel_users: type  # integer the maximum amount of users in a video channel
    approximate_member_count: type  # integer approximate number of members in this guild, returned from the GET /guilds/<id> endpoint when with_counts is true
    approximate_presence_count: type  # integer approximate number of non-offline members in this guild, returned from the GET /guilds/<id> endpoint when with_counts is true
    welcome_screen: type  # welcome screen object the welcome screen of a Community guild, shown to new members, returned in an Invite's guild object
    nsfw_level: type  # integer guild NSFW level
    stage_instances: type  # * array of stage instance objects Stage instances in the guild
    stickers: type  # array of sticker objects custom guild stickers

    def __str__(self):
        fields = []

        if hasattr(self, 'id'):
            fields.append(f'id={self.id}')

        if hasattr(self, 'name'):
            fields.append(f'name={self.name}')

        return f'Guild({", ".join(fields)})'

    def __repr__(self):
        return self.__str__()

    def ingest_raw_dict(self, data) -> 'Guild':
        self.from_dict(data)

        self.cache()
        return self

    def from_dict(self, data: dict) -> 'Guild':

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
                new_channel = ext_channel.ChannelImporter.ingest_raw_dict(channel_dict, self)
                self.channels.append(new_channel)

        return self

    def cache(self):
        # Preventing circular imports
        from ..utilities import Cache

        Cache().add(self)
