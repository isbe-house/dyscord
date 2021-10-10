import copy
from typing import List

from .base_object import BaseDiscordObject
from . import user, snowflake, guild


class Ready(BaseDiscordObject):

    # application: Dict[str, Union[int, str]]  # TODO: Application objects needs to exist.
    geo_ordered_rtc_regions: List[str]
    guild_join_requests: list  # TODO: See examples of this and process.
    guilds: List[guild.Guild]
    presences: list  # TODO: Get examples of this.
    private_channels: list  # TODO: Get examples of this.
    relationships: list  # TODO: Get examples of this.
    session_id: str  # Why is this not a snowflake? Dammit!
    shard_id: int  # TODO: Get examples of this.
    shard_total: int  # TODO: Get examples of this.
    user: user.User
    user_settings: dict  # TODO: Get example of this.
    version: int  # Version of the API being used.

    def __init__(self):
        '''
        We don't have an ID for these objects, so do not call the super.
        '''
        pass

    def __hash__(self):
        return hash(self.session_id)

    def __eq__(self, other):
        return self.session_id == other.session_id

    def ingest_raw_dict(self, data: dict) -> 'Ready':
        '''
        Ingest and cache a given object for future use.
        '''
        self.from_dict(data)
        return self

    def from_dict(self, data: dict) -> 'Ready':
        '''
        Parse an object from a dictionary and return it.
        '''
        self.geo_ordered_rtc_regions = copy.deepcopy(data['geo_ordered_rtc_regions'])
        self.guilds = list()
        for partial_guild_dict in data['guilds']:
            new_guild = guild.Guild()
            new_guild.id = snowflake.Snowflake(partial_guild_dict['id'])
            self.guilds.append(new_guild)
        self.session_id = data['session_id']
        self.user = user.User().ingest_raw_dict(data['user'])
        self.version = data['v']

        return self
