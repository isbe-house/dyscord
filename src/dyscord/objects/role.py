from typing import Any, Optional

from .base_object import BaseDiscordObject

from . import snowflake


class Role(BaseDiscordObject):
    '''Roles represent a set of permissions attached to a group of users.'''

    id: snowflake.Snowflake
    name: str
    color: int  # integer representation of hexadecimal color code
    hoist: bool  # if this role is pinned in the user listing
    icon: str   # role icon hash
    unicode_emoji: str  # role unicode emoji
    position: int   # position of this role
    permissions: str    # permission bit set
    managed: bool    # whether this role is managed by an integration
    mentionable: bool    # whether this role is mentionable
    tags: Optional['RoleTags']   # tags object	the tags this role has

    def from_dict(self, data: dict) -> 'Role':
        '''Parse a Role from an API compliant dict.'''
        self.id = snowflake.Snowflake(data['id'])
        self.name = data['name']
        self.color = data['color']
        self.hoist = data['hoist']
        self.position = data['position']
        self.permissions = data['permissions']
        self.managed = data['managed']
        self.mentionable = data['mentionable']

        if 'icon' in data:
            self.icon = data['icon']

        if 'unicode_emoji' in data:
            self.unicode_emoji = data['unicode_emoji']

        if 'tags' in data:
            self.tags = RoleTags().from_dict(data['tags'])

        return self


class RoleTags(BaseDiscordObject):
    '''RoleTags.'''

    bot_id: snowflake.Snowflake
    integration_id: snowflake.Snowflake
    premium_subscriber: Any

    def from_dict(self, data: dict) -> 'RoleTags':
        '''Parse a RoleRags from an API compliant dict.'''
        if 'bot_id' in data:
            self.bot_id = data['bot_id']

        if 'integration_id' in data:
            self.integration_id = data['integration_id']

        if 'premium_subscriber' in data:
            self.premium_subscriber = data['premium_subscriber']

        return self
