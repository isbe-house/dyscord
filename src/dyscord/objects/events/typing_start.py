from datetime import datetime
from typing import Optional

from ..base_object import BaseDiscordObject
from .. import snowflake
from ... import objects


class TypingStart(BaseDiscordObject):
    '''Event given when a user starts to type.

    Attributes:
        channel_id (Snowflake): ID of the typing event.
        guild_id (Snowflake): Guild ID of the typing event.
        user_id (Snowflake): user_id of the user which started to type.
        timestamp (datetime): Datetime the user started typing.
        member (Member): Member that started typing.
    '''

    channel_id: 'objects.Snowflake' = None  # type: ignore
    guild_id: 'Optional[objects.Snowflake]' = None  # type: ignore
    user_id: 'objects.Snowflake' = None  # type: ignore
    timestamp: datetime = None  # type: ignore
    member: 'Optional[objects.Member]' = None  # type: ignore

    def from_dict(self, data: dict) -> 'TypingStart':
        '''Parse a TypingStart from an API compliant dict.'''
        if 'channel_id' in data:
            self.channel_id = snowflake.Snowflake(data['channel_id'])
        if 'guild_id' in data:
            self.guild_id = snowflake.Snowflake(data['guild_id'])
        if 'user_id' in data:
            self.user_id = snowflake.Snowflake(data['user_id'])
        if 'timestamp' in data:
            self.timestamp = datetime.fromtimestamp(data['timestamp'])
        if 'member' in data:
            self.member = objects.Member().from_dict(data['member'])
        return self
