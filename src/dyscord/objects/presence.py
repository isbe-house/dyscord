from typing import Optional, List
from .base_object import BaseDiscordObject
from . import user as ext_user, snowflake, activity as ext_activity


class Presence(BaseDiscordObject):
    '''Presence.'''

    user: 'ext_user.User' = None  # type: ignore # user object the user presence is being updated for
    guild_id: 'snowflake.Snowflake' = None  # type: ignore # snowflake id of the guild
    status: 'str' = None  # type: ignore # string either "idle", "dnd", "online", or "offline"
    activities: 'List[ext_activity.Activity]' = None  # type: ignore # array of activity objects user's current activities
    client_status: 'ClientStatus' = None  # type: ignore # client_status object user's platform-dependent status

    @property
    def _auto_map(self):
        return {
            'user': ext_user.User,
            'guild_id': snowflake.Snowflake,
            'status': str,
            'activities': [ext_activity.Activity],
            'client_status': ClientStatus,
        }


class ClientStatus(BaseDiscordObject):
    '''ClientStatus.'''

    desktop: 'Optional[str]' = None  # tpye: ignore # string the user's status set for an active desktop (Windows, Linux, Mac) application session
    mobile: 'Optional[str]' = None  # tpye: ignore # string the user's status set for an active mobile (iOS, Android) application session
    web: 'Optional[str]' = None  # tpye: ignore # string the user's status set for an active web (browser, bot account) application session

    @property
    def _auto_map(self):
        return {
            'desktop': str,
            'mobile': str,
            'web': str,
        }
