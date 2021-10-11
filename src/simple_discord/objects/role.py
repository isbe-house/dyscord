from typing import Any

from .base_object import BaseDiscordObject

from . import snowflake


class Role(BaseDiscordObject):
    '''Roles represent a set of permissions attached to a group of users.'''

    id: snowflake.Snowflake
    name: str
    color: int  #	integer	integer representation of hexadecimal color code
    hoist: bool  #	boolean	if this role is pinned in the user listing
    icon: str   #?	?string	role icon hash
    unicode_emoji: str  #?	?string	role unicode emoji
    position: int   #	integer	position of this role
    permissions: str    #	string	permission bit set
    managed: bool    #	boolean	whether this role is managed by an integration
    mentionable: bool    #	boolean	whether this role is mentionable
    tags: str   #?	role tags object	the tags this role has

class RoleTags(BaseDiscordObject):

    bot_id: snowflake.Snowflake
    integration_id: snowflake.Snowflake
    premium_subscriber: Any
