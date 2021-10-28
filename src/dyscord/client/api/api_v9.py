import asyncio
import datetime
from pprint import pprint

import cachetools
import cachetools.keys
import httpx

from ...objects.snowflake import Snowflake

from ...utilities import Log

from ... import objects


class API_V9:
    '''Version 9 of the discord API.'''

    BASE_URL = 'https://discord.com/api/v9'
    TOKEN: str  # Overridden when the API is loaded in DiscordClient._connect
    APPLICATION_ID: str
    USER_AGENT: str = 'Discord Bot ()'

    _lock = asyncio.Lock()
    _log = Log()
    _ttl_cache: dict = cachetools.TTLCache(10_000, ttl=datetime.timedelta(minutes=15), timer=datetime.datetime.now)  # type: ignore

    @classmethod
    def _auth_header(cls):
        return {'Authorization': f'Bot {cls.TOKEN}', 'Content-Type': 'application/json'}

    @classmethod
    async def _handle_rate_limit(cls, response):
        headers = response.headers

        if 'x-ratelimit-reset' not in headers:
            return

        reset_datetime = datetime.datetime.fromtimestamp(float(headers['x-ratelimit-reset']))
        time_until_reset = reset_datetime - datetime.datetime.now()

        if int(headers["x-ratelimit-remaining"]) == 0:
            cls._log.warning(f'Rate limit encountered, waiting for {time_until_reset}.')
            await asyncio.sleep(time_until_reset.total_seconds())

    @classmethod
    async def _invoke_method(cls, method):
        async with cls._lock:
            r = await method
            try:
                r.raise_for_status()
            except Exception:
                cls._log.exception(r.content)
                raise
            await cls._handle_rate_limit(r)
        return r

    # GATEWAY ENDPOINTS

    @classmethod
    async def get_gateway_bot(cls, token: str) -> dict:
        '''Get URL of the gateway for bots.'''
        if not isinstance(token, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(token)}] for token.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f'{cls.BASE_URL}/gateway/bot',
                    headers={'Authorization': f'Bot {token}'},
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)

        # Add our own settings to URI
        data = r.json()
        data['url'] += '?v=9&encoding=json'

        return data

    @classmethod
    async def get_gateway(cls) -> dict:
        '''Get URL of the gateway.'''
        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.get(f'{cls.BASE_URL}/gateway')
                r.raise_for_status()
            await cls._handle_rate_limit(r)

        return r.json()

    @classmethod
    async def get_global_application_commands(cls):
        '''Get all global application commands.'''
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/commands'

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    url,
                    headers=cls._auth_header(),
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def create_global_application_command(cls, command_structure: dict):
        '''Create or update a global application command.'''
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/commands'

        if not isinstance(command_structure, (dict,)):
            raise TypeError(f'Got illegal type [{type(command_structure)}] for command_structure.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    url,
                    headers=cls._auth_header(),
                    json=command_structure,
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def get_global_application_command(cls, command_id: 'objects.Snowflake'):
        '''Get a global application command.'''
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/commands/{command_id}'

        if not isinstance(command_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(command_id)}] for command_id.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    url,
                    headers=cls._auth_header(),
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def edit_global_application_command(cls,
                                              command_id: 'objects.Snowflake',
                                              command_structure: dict
                                              ):
        '''Edit a global application command.'''
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/commands/{command_id}'

        if not isinstance(command_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(command_id)}] for command_id.')
        if not isinstance(command_structure, (dict,)):
            raise TypeError(f'Got illegal type [{type(command_structure)}] for command_structure.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.patch(
                    url,
                    headers=cls._auth_header(),
                    json=command_structure,
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def delete_global_application_command(cls, command_id: 'objects.Snowflake'):
        '''Delete a global application command.'''
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/commands/{command_id}'

        if not isinstance(command_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(command_id)}] for command_id.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.delete(
                    url,
                    headers=cls._auth_header(),
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)

    @classmethod
    async def bulk_overwrite_global_application_commands(cls, command_id: 'objects.Snowflake'):
        '''Unimplemented.'''
        # PUT/applications/{application.id}/commands
        raise NotImplementedError('TBD')

    @classmethod
    async def get_guild_application_commands(cls, guild_id: 'objects.Snowflake'):
        '''Get all application commands from a specific guild.'''
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/guilds/{guild_id}/commands'

        if not isinstance(guild_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(guild_id)}] for guild_id.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    url,
                    headers=cls._auth_header(),
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def create_guild_application_command(cls,
                                               guild_id: 'objects.Snowflake',
                                               command_structure: dict
                                               ) -> dict:
        '''Create a guild appplication command.'''
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/guilds/{guild_id}/commands'

        if not isinstance(guild_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(guild_id)}] for guild_id.')
        if not isinstance(command_structure, (dict,)):
            raise TypeError(f'Got illegal type [{type(command_structure)}] for command_structure.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    url,
                    headers=cls._auth_header(),
                    json=command_structure,
                )
                try:
                    r.raise_for_status()
                except Exception:
                    pprint(command_structure)
                    pprint(r.json())
                    raise
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def get_guild_application_command(cls,
                                            guild_id: 'objects.Snowflake',
                                            command_id: 'objects.Snowflake',
                                            ) -> dict:
        '''Get a specific guild application command.'''
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/guilds/{guild_id}/commands/{command_id}'

        if not isinstance(guild_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(guild_id)}] for guild_id.')
        if not isinstance(command_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(command_id)}] for command_id.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    url,
                    headers=cls._auth_header(),
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def edit_guild_application_command(cls,
                                             guild_id: 'objects.Snowflake',
                                             command_id: 'objects.Snowflake',
                                             command_structure: dict,
                                             ):
        '''Edit a guild application command.'''
        # PATCH /applications/{application.id}/guilds/{guild.id}/commands/{command.id}
        raise NotImplementedError('TBD')

    @classmethod
    async def delete_guild_application_command(cls,
                                               guild_id: 'objects.Snowflake',
                                               command_id: 'objects.Snowflake',
                                               ) -> None:
        '''Delete an application command.'''
        url = f'{cls.BASE_URL}/applications/{cls.APPLICATION_ID}/guilds/{guild_id}/commands/{command_id}'

        if not isinstance(guild_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(guild_id)}] for guild_id.')
        if not isinstance(command_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(command_id)}] for command_id.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.delete(
                    url,
                    headers=cls._auth_header(),
                )
                try:
                    r.raise_for_status()
                except Exception:
                    pprint(r.json())
                    raise
            await cls._handle_rate_limit(r)

    @classmethod
    async def bulk_overwrite_guild_application_command(cls,
                                                       guild_id: 'objects.Snowflake',
                                                       command_id: 'objects.Snowflake',
                                                       command_structure: dict,
                                                       ):
        '''TODO: Copy from api docs.'''
        # PUT /applications/{application.id}/guilds/{guild.id}/commands/{command.id}
        raise NotImplementedError('TBD')

    # Interaction Methods
    '''
    '''

    @classmethod
    async def create_interaction_response(cls,
                                          interaction_id: 'objects.Snowflake',
                                          interaction_token: str,
                                          data_structure: dict,
                                          ) -> None:
        '''TODO: Copy from api docs.'''
        url = f'{cls.BASE_URL}/interactions/{interaction_id}/{interaction_token}/callback'

        if not isinstance(interaction_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(interaction_id)}] for interaction_id.')
        if not isinstance(interaction_token, (str, )):
            raise TypeError(f'Got illegal type [{type(interaction_token)}] for interaction_token.')
        if not isinstance(data_structure, (dict, )):
            raise TypeError(f'Got illegal type [{type(data_structure)}] for data_structure.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    url,
                    json=data_structure
                )
                try:
                    r.raise_for_status()
                except Exception:
                    print(r.content)
                    raise
            await cls._handle_rate_limit(r)

    @classmethod
    async def get_original_interaction_response(cls,
                                                interaction_token: str,
                                                ) -> dict:
        '''TODO: Copy from api docs.'''
        url = f'{cls.BASE_URL}/webhooks/{cls.APPLICATION_ID}/{interaction_token}/messages/@origional'

        if not isinstance(interaction_token, (str, )):
            raise TypeError(f'Got illegal type [{type(interaction_token)}] for interaction_token.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    url,
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def edit_original_interaction_response(cls,
                                                 interaction_token: str,
                                                 data_structure: dict,
                                                 ) -> None:
        '''Edit Original Interaction Response.

        PATCH/webhooks/{application.id}/{interaction.token}/messages/@original

        Edits the initial Interaction response. Functions the same as Edit Webhook Message.
        '''
        url = f'{cls.BASE_URL}/webhooks/{cls.APPLICATION_ID}/{interaction_token}/messages/@original'

        if not isinstance(interaction_token, (str, )):
            raise TypeError(f'Got illegal type [{type(interaction_token)}] for interaction_token.')
        if not isinstance(data_structure, (dict, )):
            raise TypeError(f'Got illegal type [{type(data_structure)}] for data_structure.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.patch(
                    url,
                    json=data_structure
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)

    @classmethod
    async def delete_original_interaction_response(cls,
                                                   interaction_token: str,
                                                   ) -> None:
        '''Delete Original Interaction Response.

        DELETE/webhooks/{application.id}/{interaction.token}/messages/@original

        Deletes the initial Interaction response. Returns 204 on success.
        '''
        url = f'{cls.BASE_URL}/webhooks/{cls.APPLICATION_ID}/{interaction_token}/messages/@original'

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.delete(
                    url,
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)

        if not isinstance(interaction_token, (str, )):
            raise TypeError(f'Got illegal type [{type(interaction_token)}] for interaction_token.')

    @classmethod
    async def create_followup_message(cls,
                                      interaction_token: str,
                                      data_structure: dict,
                                      ) -> dict:
        '''Create Followup Message.

        POST/webhooks/{application.id}/{interaction.token}

        Create a followup message for an Interaction. Functions the same as Execute Webhook, but wait is always true,
        and flags can be set to 64 in the body to send an ephemeral message. The thread_id query parameter is not required
        (and is furthermore ignored) when using this endpoint for interaction followups.
        '''
        url = f'{cls.BASE_URL}/webhooks/{cls.APPLICATION_ID}/{interaction_token}'

        if not isinstance(interaction_token, (str, )):
            raise TypeError(f'Got illegal type [{type(interaction_token)}] for interaction_token.')
        if not isinstance(data_structure, (dict,)):
            raise TypeError(f'Got illegal type [{type(data_structure)}] for data_structure.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    url,
                    json=data_structure
                )
                try:
                    r.raise_for_status()
                except Exception:
                    print(r)
                    raise
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def get_followup_message(cls,
                                   interaction_token: str,
                                   message_id: 'Snowflake',
                                   ) -> dict:
        '''Get Followup Message.

        GET/webhooks/{application.id}/{interaction.token}/messages/{message.id}

        Returns a followup message for an Interaction. Functions the same as Get Webhook Message. Does not support ephemeral followups.
        '''
        url = f'{cls.BASE_URL}/webhooks/{cls.APPLICATION_ID}/{interaction_token}/messages/{message_id}'

        if not isinstance(interaction_token, (str, )):
            raise TypeError(f'Got illegal type [{type(interaction_token)}] for interaction_token.')
        if not isinstance(message_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(message_id)}] for message_id.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    url
                )
                try:
                    r.raise_for_status()
                except Exception:
                    print(r)
                    raise
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def edit_followup_message(cls,
                                    interaction_token: str,
                                    message_id: 'Snowflake',
                                    data_structure: dict,
                                    ) -> dict:
        '''Edit Followup Message.

        PATCH/webhooks/{application.id}/{interaction.token}/messages/{message.id}

        Edits a followup message for an Interaction. Functions the same as Edit Webhook Message. Does not support ephemeral followups.
        '''
        url = f'{cls.BASE_URL}/webhooks/{cls.APPLICATION_ID}/{interaction_token}/messages/{message_id}'

        if not isinstance(interaction_token, (str, )):
            raise TypeError(f'Got illegal type [{type(interaction_token)}] for interaction_token.')
        if not isinstance(message_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(message_id)}] for message_id.')
        if not isinstance(data_structure, (dict, )):
            raise TypeError(f'Got illegal type [{type(data_structure)}] for data_structure.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.patch(
                    url,
                    json=data_structure
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)
        return r.json()

    @classmethod
    async def delete_followup_message(cls,
                                      interaction_token: str,
                                      message_id: 'Snowflake',
                                      ) -> None:
        '''Delete Followup Message.

        DELETE/webhooks/{application.id}/{interaction.token}/messages/{message.id}

        Deletes a followup message for an Interaction. Returns 204 on success. Does not support ephemeral followups.
        '''
        url = f'{cls.BASE_URL}/webhooks/{cls.APPLICATION_ID}/{interaction_token}/messages/{message_id}'

        if not isinstance(interaction_token, (str,)):
            raise TypeError(f'Got illegal type [{type(interaction_token)}] for interaction_token.')
        if not isinstance(message_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(message_id)}] for message_id.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.delete(
                    url
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)

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

    # Channel methods

    @classmethod
    async def get_channel(cls, channel_id: 'objects.Snowflake') -> dict:
        '''Get channel by ID.'''
        url = f'{cls.BASE_URL}/channels/{channel_id}'

        if not isinstance(channel_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(channel_id)}] for channel_id.')

        try:
            return cls._ttl_cache[cachetools.keys.hashkey('get_channel', channel_id)]
        except KeyError:
            pass

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    url,
                    headers=cls._auth_header(),
                )
                r.raise_for_status()
            await cls._handle_rate_limit(r)
        cls._ttl_cache[cachetools.keys.hashkey('get_channel', channel_id)] = r.json()
        return r.json()

    @classmethod
    async def create_message(cls,
                             channel_id: 'objects.Snowflake',
                             message_payload: dict,
                             ):
        '''TODO: Copy from api docs.'''
        url = f'{cls.BASE_URL}/channels/{channel_id}/messages'

        if not isinstance(channel_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(channel_id)}] for channel_id.')
        if not isinstance(message_payload, (dict,)):
            raise TypeError(f'Got illegal type [{type(message_payload)}] for message_payload.')

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    url,
                    headers=cls._auth_header(),
                    json=message_payload,
                )
                try:
                    r.raise_for_status()
                except Exception:
                    cls._log.exception(r.content)
                    raise
            await cls._handle_rate_limit(r)
        return r.json()

    # Guild methods

    @classmethod
    async def get_guild(cls, guild_id: 'objects.Snowflake') -> dict:
        '''Get guilds.

        TODO: Document this.
        '''
        url = f'{cls.BASE_URL}/guilds/{guild_id}'

        if not isinstance(guild_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(guild_id)}] for guild_id.')

        try:
            return cls._ttl_cache[cachetools.keys.hashkey('get_guild', guild_id)]
        except KeyError:
            pass

        async with cls._lock:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    url,
                    headers=cls._auth_header(),
                )
                try:
                    r.raise_for_status()
                except Exception:
                    cls._log.exception(r.content)
                    raise
            await cls._handle_rate_limit(r)
        cls._ttl_cache[cachetools.keys.hashkey('get_guild', guild_id)] = r.json()
        return r.json()

    @classmethod
    async def get_guild_roles(cls, guild_id: 'Snowflake') -> dict:
        '''Get Guild Roles.

        GET/guilds/{guild.id}/roles

        Returns a list of role objects for the guild.
        '''
        url = f'{cls.BASE_URL}/guilds/{guild_id}/roles'

        if not isinstance(guild_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(guild_id)}] for guild_id.')

        try:
            return cls._ttl_cache[cachetools.keys.hashkey('get_guild_roles', guild_id)]
        except KeyError:
            pass

        async with httpx.AsyncClient() as client:
            method = client.get(url, headers=cls._auth_header())
            r = await cls._invoke_method(method)
        cls._ttl_cache[cachetools.keys.hashkey('get_guild_roles', guild_id)] = r.json()
        return r.json()

    # User methods

    @classmethod
    async def get_current_user(cls) -> dict:
        '''Get Current User.

        GET/users/@me

        Returns the user object of the requester's account. For OAuth2, this requires the identify scope, which will return the object without an email,
        and optionally the email scope, which returns the object with an email.
        '''
        url = f'{cls.BASE_URL}/users/@me'

        async with httpx.AsyncClient() as client:
            method = client.get(url, headers=cls._auth_header())
            r = await cls._invoke_method(method)
        return r.json()

    @classmethod
    async def get_user(cls, user_id: 'Snowflake') -> dict:
        '''Get User.

        GET/users/{user.id}

        Returns a user object for a given user ID.
        '''
        url = f'{cls.BASE_URL}/users/{user_id}'

        if not isinstance(user_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(user_id)}] for user_id.')

        try:
            return cls._ttl_cache[cachetools.keys.hashkey('get_user', user_id)]
        except KeyError:
            pass

        async with httpx.AsyncClient() as client:
            method = client.get(url, headers=cls._auth_header())
            r = await cls._invoke_method(method)
        cls._ttl_cache[cachetools.keys.hashkey('get_user', user_id)] = r.json()
        return r.json()

    @classmethod
    async def create_dm(cls, recipient_id: 'Snowflake') -> dict:
        '''Create DM.

        POST/users/@me/channels

        Create a new DM channel with a user. Returns a DM channel object.
        '''
        url = f'{cls.BASE_URL}/users/@me/channels'

        if not isinstance(recipient_id, (str, Snowflake)):
            raise TypeError(f'Got illegal type [{type(recipient_id)}] for recipient_id.')

        async with httpx.AsyncClient() as client:
            method = client.post(url,
                                 json={'recipient_id': recipient_id},
                                 headers=cls._auth_header(),
                                 )
            r = await cls._invoke_method(method)
        return r.json()

    '''
    Modify Current User
        PATCH/users/@me
        Modify the requester's user account settings. Returns a user object on success.

    Get Current User Guilds
        GET/users/@me/guilds
        Returns a list of partial guild objects the current user is a member of. Requires the guilds OAuth2 scope.

    Leave Guild
        DELETE/users/@me/guilds/{guild.id}
        Leave a guild. Returns a 204 empty response on success.

    Get User Connections
        GET/users/@me/connections
        Returns a list of connection objects. Requires the connections OAuth2 scope.
    '''  # noqa: E501

    # Webhook methods

    '''
    Create Webhook
        POST/channels/{channel.id}/webhooks

    Get Channel Webhooks
        GET/channels/{channel.id}/webhooks

    Get Guild Webhooks
        GET/guilds/{guild.id}/webhooks

    Get Webhook
        GET/webhooks/{webhook.id}

    Get Webhook with Token
        GET/webhooks/{webhook.id}/{webhook.token}

    Modify Webhook
        PATCH/webhooks/{webhook.id}

    Modify Webhook with Token
        PATCH/webhooks/{webhook.id}/{webhook.token}

    Delete Webhook
        DELETE/webhooks/{webhook.id}

    Delete Webhook with Token
        DELETE/webhooks/{webhook.id}/{webhook.token}

    Execute Webhook
        POST/webhooks/{webhook.id}/{webhook.token}

    Execute Slack-Compatible Webhook
        POST/webhooks/{webhook.id}/{webhook.token}/slack

    Execute GitHub-Compatible Webhook
        POST/webhooks/{webhook.id}/{webhook.token}/github

    Get Webhook Message
        GET/webhooks/{webhook.id}/{webhook.token}/messages/{message.id}

    Edit Webhook Message
        PATCH/webhooks/{webhook.id}/{webhook.token}/messages/{message.id}

    Delete Webhook Message
        DELETE/webhooks/{webhook.id}/{webhook.token}/messages/{message.id}
    '''  # noqa: E501
