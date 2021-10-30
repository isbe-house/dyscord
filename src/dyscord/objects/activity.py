from typing import Optional, List
from datetime import datetime

from .base_object import BaseDiscordObject
from . import snowflake, enumerations


class Activity(BaseDiscordObject):
    '''Activity.'''

    id: str = None  # type: ignore # UNDOCUMENTED General ID for the given activity
    name: str = None  # type: ignore # string the activity's name
    type: enumerations.ACTIVITY_TYPE = None  # type: ignore # integer activity type
    url: Optional[str] = None  # type: ignore #? ?string stream url, is validated when type is 1
    created_at: datetime = None  # type: ignore # integer unix timestamp (in milliseconds) of when the activity was added to the user's session
    timestamps: 'Optional[TimeStamps]' = None  # type: ignore #? timestamps object unix timestamps for start and/or end of the game
    application_id: 'Optional[snowflake.Snowflake]' = None  # type: ignore #? snowflake application id for the game
    details: Optional[str] = None  # type: ignore #? ?string what the player is currently doing
    state: 'Optional[str]' = None  # type: ignore #? ?string the user's current party status
    emoji: 'Optional[ActivityEmoji]' = None  # type: ignore #? ?emoji object the emoji used for a custom status
    party: 'Optional[Party]' = None  # type: ignore #? party object information for the current party of the player
    assets: 'Optional[Assets]' = None  # type: ignore #? assets object images for the presence and their hover texts
    secrets: 'Optional[Secrets]' = None  # type: ignore #? secrets object secrets for Rich Presence joining and spectating
    instance: 'Optional[bool]' = None  # type: ignore #? boolean whether or not the activity is an instanced game session
    flags: 'Optional[enumerations.ACTIVITY_FLAGS]' = None  # type: ignore #? integer activity flags ORd together, describes what the payload includes
    buttons: 'Optional[List[Buttons]]' = None  # type: ignore #? array of buttons the custom buttons shown in the Rich Presence (max 2)

    @property
    def _auto_map(self):
        return {
            'id': str,
            'name': str,
            'type': enumerations.ACTIVITY_TYPE,
            'url': str,
            'created_at': self._fromtimestamp_milliseconds,
            'timestamps': TimeStamps,
            'application_id': snowflake.Snowflake,
            'details': str,
            'state': str,
            'emoji': ActivityEmoji,
            'party': Party,
            'assets': Assets,
            'secrets': Secrets,
            'instance': bool,
            'flags': enumerations.ACTIVITY_FLAGS,
            'buttons': [Buttons],
        }


class TimeStamps(BaseDiscordObject):
    '''TimeStamps.'''

    start: 'Optional[datetime]' = None  # type: ignore
    end: 'Optional[datetime]' = None  # type: ignore

    @property
    def _auto_map(self):
        return {
            'start': self._fromtimestamp_milliseconds,
            'end': self._fromtimestamp_milliseconds,
        }


class Party(BaseDiscordObject):
    '''Party.'''

    id: 'str' = None  # type: ignore
    size: 'Optional[List[int]]' = None

    @property
    def _auto_map(self):
        return {
            'id': str,
            'size': [int],
        }


class Assets(BaseDiscordObject):
    '''Assets.'''

    large_image: 'Optional[str]' = None  # type: ignore # The id for a large asset of the activity, usually a snowflake
    large_text: 'Optional[str]' = None  # type: ignore # Text displayed when hovering over the large image of the activity
    small_image: 'Optional[str]' = None  # type: ignore # The id for a small asset of the activity, usually a snowflake
    small_text: 'Optional[str]' = None  # type: ignore # Text displayed when hovering over the small image of the activity

    @property
    def _auto_map(self):
        return {
            'large_image': str,
            'large_text': str,
            'small_image': str,
            'small_text': str,
        }


class Secrets(BaseDiscordObject):
    '''Secrets.'''

    join: 'Optional[str]' = None  # type: ignore # the secret for joining a party
    spectate: 'Optional[str]' = None  # type: ignore # the secret for spectating a game
    match: 'Optional[str]' = None  # type: ignore # the secret for a specific instanced match

    @property
    def _auto_map(self):
        return {
            'join': str,
            'spectate': str,
            'match': str,
        }


class Buttons(BaseDiscordObject):
    '''Buttons.'''

    label: 'Optional[str]' = None  # the text shown on the button (1-32 characters)
    url: 'Optional[str]' = None  # the url opened when clicking the button (1-512 characters)

    @property
    def _auto_map(self):
        return {
            'join': str,
            'spectate': str,
            'match': str,
        }


class ActivityEmoji(BaseDiscordObject):
    '''ActivityEmoji.'''

    name: 'str' = None  # type: ignore # string the name of the emoji
    id: 'snowflake.Snowflake' = None  # type: ignore # snowflake the id of the emoji
    animated: 'Optional[bool]' = None  # boolean whether this emoji is animated

    @property
    def _auto_map(self):
        return {
            'name': str,
            'id': snowflake.Snowflake,
            'animated': bool,
        }
