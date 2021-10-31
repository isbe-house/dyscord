from datetime import datetime
from typing import List, Optional
import copy

from ..base_object import BaseDiscordObject
from .. import snowflake, user as ext_user


class GuildMemberUpdate(BaseDiscordObject):
    '''GuildMemberUpdate.

    Attributes:
        roles ([Snowflake]): DEPRECATED: This will be replaced with a `Role` object soon.
        guild_id (Snowflake): The ID of the guild.
        user (User): A partial user object.
        nick (str): Nickname of the `user` in the guild.
        avatar (str): Members guild avatar hash.
        joined_at (datetime): When the user joined the guild.
        premium_since (datetime): When the user started boosting the guild.
        deaf (bool): Whether the user is deafened in voice channels.
        mute (bool): Whether the user is muted in voice channels.
        pending (bool): Whether the user has not yet passed the guild's Membership Screening requirements.
    '''

    guild_id: 'snowflake.Snowflake' = None  # type: ignore
    roles: 'List[snowflake.Snowflake]' = None  # type: ignore
    user: 'ext_user.User' = None  # type: ignore
    nick: 'Optional[str]' = None  # type: ignore
    avatar: 'Optional[str]' = None  # type: ignore
    joined_at: 'Optional[datetime]' = None  # type: ignore
    premium_since: 'Optional[datetime]' = None  # type: ignore
    deaf: 'Optional[bool]' = None  # type: ignore
    mute: 'Optional[bool]' = None  # type: ignore
    pending: 'Optional[bool]' = None  # type: ignore
    is_pending: 'Optional[bool]' = None  # type: ignore

    @property
    def _auto_map(self):
        return {
            'guild_id': snowflake.Snowflake,
            'roles': [snowflake.Snowflake],
            'user': ext_user.User,
            'nick': str,
            'avatar': str,
            'joined_at': datetime.fromisoformat,
            'premium_since': datetime.fromisoformat,
            'deaf': bool,
            'mute': bool,
            'pending': bool,
            'hoisted_role': copy.copy,
            'is_pending': bool,
        }
