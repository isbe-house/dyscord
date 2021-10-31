from typing import Optional
from datetime import datetime

from ..base_object import BaseDiscordObject
from .. import snowflake, user as ext_user


class VoiceState(BaseDiscordObject):
    '''VoiceState.'''

    guild_id: 'Optional[snowflake.Snowflake]' = None  # type: ignore # ? snowflake the guild id this voice state is for
    channel_id: 'Optional[snowflake.Snowflake]' = None  # type: ignore #  ?snowflake the channel id this user is connected to
    user_id: 'snowflake.Snowflake' = None  # type: ignore #  snowflake the user id this voice state is for
    member: 'Optional[ext_user.Member]' = None  # type: ignore # ? guild member object the guild member this voice state is for
    session_id: 'str' = None  # type: ignore #  string the session id for this voice state
    deaf: 'bool' = None  # type: ignore #  boolean whether this user is deafened by the server
    mute: 'bool' = None  # type: ignore #  boolean whether this user is muted by the server
    self_deaf: 'bool' = None  # type: ignore #  boolean whether this user is locally deafened
    self_mute: 'bool' = None  # type: ignore #  boolean whether this user is locally muted
    self_stream: 'Optional[bool]' = None  # type: ignore # ? boolean whether this user is streaming using "Go Live"
    self_video: 'bool' = None  # type: ignore #  boolean whether this user's camera is enabled
    suppress: 'bool' = None  # type: ignore #  boolean whether this user is muted by the current user
    request_to_speak_timestamp: 'Optional[datetime]' = None  # type: ignore #  ?ISO8601 timestamp the time at which the user requested to speak

    @property
    def _auto_map(self):
        return {
            'guild_id': snowflake.Snowflake,
            'channel_id': snowflake.Snowflake,
            'user_id': snowflake.Snowflake,
            'member': ext_user.Member,
            'session_id': str,
            'deaf': bool,
            'mute': bool,
            'self_deaf': bool,
            'self_mute': bool,
            'self_stream': bool,
            'self_video': bool,
            'suppress': bool,
            'request_to_speak_timestamp': datetime.fromtimestamp,
        }
