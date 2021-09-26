import httpx
import orjson as json

from ...utilities import Log

from ...objects import snowflake


class API_V9:

    BASE_URL = 'https://discord.com/api/v9'
    TOKEN: str  # Overridden when the API is loaded in DiscordClient._connect
    APPLICATION_ID: str

    _log = Log()

    @classmethod
    def auth_header(cls):
        return {'Authorization': f'Bot {cls.TOKEN}'}

    # GATEWAY ENDPOINTS
    @classmethod
    async def get_gateway_bot(cls, token) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f'{cls.BASE_URL}/gateway/bot',
                headers={'Authorization': f'Bot {token}'},
            )
            r.raise_for_status()

        # Add our own settings to URI
        data = json.loads(r.content)
        data['url'] += '?v=9&encoding=json'

        return data

    @classmethod
    async def get_gateway(cls) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.get(f'{cls.BASE_URL}/gateway')
            r.raise_for_status()

        return json.loads(r.content)

    @classmethod
    async def get_global_application_commands(cls):
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/commands'

        async with httpx.AsyncClient() as client:
            r = await client.get(
                url,
                headers=cls.auth_header(),
            )
            r.raise_for_status()
        return r.json()

    @classmethod
    async def create_global_application_command(cls, command_structure: dict):
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/commands'

        from pprint import pprint
        pprint(command_structure)

        # if 'description' in command_structure and command_structure['type'] is not 1:
        #     cls._log.warning('The API sucks, and only tells you later that description fields are not allowed for type 2 and 3.')
        #     cls._log.warning('In an effort to make this easier, we just purge this here.')
        #     del command_structure['description']

        async with httpx.AsyncClient() as client:
            r = await client.post(
                url,
                headers=cls.auth_header(),
                json=command_structure,
            )
            pprint(r.json())
            r.raise_for_status()
        return r.json()

    @classmethod
    async def get_global_application_command(cls, command_id: snowflake.Snowflake):
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/commands/{command_id}'

        async with httpx.AsyncClient() as client:
            r = await client.get(
                url,
                headers=cls.auth_header(),
            )
            r.raise_for_status()
        return r.json()

    @classmethod
    async def edit_global_application_command(cls,
                                              command_id: snowflake.Snowflake,
                                              command_structure: dict
                                              ):
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/commands/{command_id}'

        async with httpx.AsyncClient() as client:
            r = await client.patch(
                url,
                headers=cls.auth_header(),
                json=command_structure,
            )
            r.raise_for_status()
        return r.json()

    @classmethod
    async def delete_global_application_command(cls, command_id: snowflake.Snowflake):
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/commands/{command_id}'

        async with httpx.AsyncClient() as client:
            r = await client.delete(
                url,
                headers=cls.auth_header(),
            )
            r.raise_for_status()

    @classmethod
    async def bulk_overwrite_global_application_commands(cls, command_id: snowflake.Snowflake):
        # PUT/applications/{application.id}/commands
        raise NotImplementedError('TBD')

    @classmethod
    async def get_guild_application_commands(cls, guild_id: snowflake.Snowflake):
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/guilds/{guild_id}/commands'

        async with httpx.AsyncClient() as client:
            r = await client.get(
                url,
                headers=cls.auth_header(),
            )
            r.raise_for_status()
        return r.json()

    @classmethod
    async def create_guild_application_command(cls,
                                               guild_id: snowflake.Snowflake,
                                               command_structure: dict
                                               ):
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/guilds/{guild_id}/commands'

        async with httpx.AsyncClient() as client:
            r = await client.post(
                url,
                headers=cls.auth_header(),
                json=command_structure,
            )
            r.raise_for_status()
        cls._log.info(r.content)

    @classmethod
    async def get_guild_application_command(cls,
                                            guild_id: snowflake.Snowflake,
                                            command_id: snowflake.Snowflake,
                                            ):
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/guilds/{guild_id}/commands/{command_id}'

        async with httpx.AsyncClient() as client:
            r = await client.get(
                url,
                headers=cls.auth_header(),
            )
            r.raise_for_status()
        return r.json()

    @classmethod
    async def edit_guild_application_command(cls,
                                             guild_id: snowflake.Snowflake,
                                             command_id: snowflake.Snowflake,
                                             command_structure: dict,
                                             ):
        # PATCH /applications/{application.id}/guilds/{guild.id}/commands/{command.id}
        raise NotImplementedError('TBD')

    @classmethod
    async def delete_guild_application_command(cls,
                                               guild_id: snowflake.Snowflake,
                                               command_id: snowflake.Snowflake,
                                               ):
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/guilds/{guild_id}/commands/{command_id}'

        async with httpx.AsyncClient() as client:
            r = await client.delete(
                url,
                headers=cls.auth_header(),
            )
            r.raise_for_status()

    @classmethod
    async def bulk_overwrite_guild_application_command(cls,
                                                       guild_id: snowflake.Snowflake,
                                                       command_id: snowflake.Snowflake,
                                                       command_structure: dict,
                                                       ):
        # PUT /applications/{application.id}/guilds/{guild.id}/commands/{command.id}
        raise NotImplementedError('TBD')

    @classmethod
    async def interaction_respond(cls,
                                  interaction_id: snowflake.Snowflake,
                                  interaction_token: str,
                                  data_structure: dict,
                                  ):
        url = f'{cls.BASE_URL}/interactions/{interaction_id}/{interaction_token}/callback'

        async with httpx.AsyncClient() as client:
            r = await client.post(
                url,
                json=data_structure
            )
            r.raise_for_status()
        cls._log.info(r.content)

    '''
    TODO: Implement the following API endpoints.

    Get Guild Application Command Permissions
        GET/applications/{application.id}/guilds/{guild.id}/commands/permissions

    Get Application Command Permissions
        GET/applications/{application.id}/guilds/{guild.id}/commands/{command.id}/permissions

    Edit Application Command Permissions
        PUT/applications/{application.id}/guilds/{guild.id}/commands/{command.id}/permissions

    Batch Edit Application Command Permissions
        PUT/applications/{application.id}/guilds/{guild.id}/commands/permissions
    '''

    @classmethod
    async def get_channel(cls, channel_id: snowflake.Snowflake):
        url = f'{cls.BASE_URL}/channels/{channel_id}'

        async with httpx.AsyncClient() as client:
            r = await client.get(
                url,
                headers=cls.auth_header(),
            )
            r.raise_for_status()

        data = json.loads(r.content)
        return data
