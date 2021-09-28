import asyncio
import time

from collections import defaultdict
from functools import wraps
from pprint import pprint
from typing import Optional

import websockets
import orjson as json

from .api import API
from .gateway_intents import Intents

from .. import utilities
from .. import objects

from .events import on_channel_create, on_channel_delete, on_channel_pins_update, on_channel_update, on_guild_ban_add, on_guild_ban_remove, on_guild_create,\
    on_guild_delete, on_guild_emojis_update, on_guild_integrations_update, on_guild_member_add, on_guild_member_remove, on_guild_member_update,\
    on_guild_role_create, on_guild_role_delete, on_guild_role_update, on_guild_stickers_update, on_guild_update, on_integration_create, on_integration_delete,\
    on_integration_update, on_invite_create, on_invite_delete, on_message_create, on_message_delete, on_message_delete_bulk, on_message_reaction_add,\
    on_message_reaction_remove, on_message_reaction_remove_all, on_message_reaction_remove_emoji, on_message_update, on_presence_update, on_ready,\
    on_stage_instance_create, on_stage_instance_delete, on_stage_instance_update, on_thread_create, on_thread_delete, on_thread_list_sync,\
    on_thread_member_update, on_thread_members_update, on_thread_update, on_typing_start, on_voice_state_update, on_webhooks_update, on_interaction_create


class DiscordClient:

    _log = utilities.Log()

    def __init__(self, token: str, application_id: Optional[str] = None):
        # Discord attributes
        self.token = token
        self.application_id = application_id
        self.intent = 0
        self.ready = False
        self.session_id: str
        self.cache = utilities.Cache()
        self.me: objects.User

        # Private attributes
        self._heartbeat_task = None
        self._last_heartbeat_ack = None
        self._listener_task = None
        self._sequence_number = None
        self._wrapper_registrations: dict = defaultdict(lambda: list())

    def configure_intents(self,  # noqa: C901
                          guilds: bool = False,
                          guild_members: bool = False,
                          guild_bans: bool = False,
                          guild_emoji_and_stickers: bool = False,
                          guild_integrations: bool = False,
                          guild_wehooks: bool = False,
                          guild_invites: bool = False,
                          guild_voice_states: bool = False,
                          guild_presences: bool = False,
                          guild_messages: bool = False,
                          guild_message_reactions: bool = False,
                          guild_message_typeing: bool = False,
                          direct_messages: bool = False,
                          direct_message_reactions: bool = False,
                          direct_messages_typeing: bool = False,
                          ):
        self.intent = 0
        if guilds:
            self.intent += Intents.GUILDS
        if guild_members:
            self.intent += Intents.GUILD_MEMBERS
        if guild_bans:
            self.intent += Intents.GUILD_BANS
        if guild_emoji_and_stickers:
            self.intent += Intents.GUILD_EMOJIS_AND_STICKERS
        if guild_integrations:
            self.intent += Intents.GUILD_INTEGRATIONS
        if guild_wehooks:
            self.intent += Intents.GUILD_WEBHOOKS
        if guild_invites:
            self.intent += Intents.GUILD_INVITES
        if guild_voice_states:
            self.intent += Intents.GUILD_VOICE_STATES
        if guild_presences:
            self.intent += Intents.GUILD_PRESENCES
        if guild_messages:
            self.intent += Intents.GUILD_MESSAGES
        if guild_message_reactions:
            self.intent += Intents.GUILD_MESSAGE_REACTIONS
        if guild_message_typeing:
            self.intent += Intents.GUILD_MESSAGE_TYPING
        if direct_messages:
            self.intent += Intents.DIRECT_MESSAGES
        if direct_message_reactions:
            self.intent += Intents.DIRECT_MESSAGE_REACTIONS
        if direct_messages_typeing:
            self.intent += Intents.DIRECT_MESSAGE_TYPING

    def run(self):
        '''
        Start the async loop and run forever.
        '''
        self._log.info('Starting...')
        self._log.info(f'Application ID: {self.application_id}')
        asyncio.run(self._run())

    async def _run(self):

        # Start up the listener
        await self._connect()

        # Sleep forever
        while True:

            await asyncio.sleep(1)

            if self._listener_task is not None:

                if self._listener_task.done():

                    exception = self._listener_task.exception()
                    if exception:
                        try:
                            raise exception
                        except Exception:
                            self._log.exception('Caught exception')
                            raise

    async def _connect(self):
        '''
        TODO: Implement connection to discord's servers.
        '''

        API.TOKEN = self.token
        if type(self.application_id) is str:
            API.APPLICATION_ID = self.application_id

        gateway_uri = (await API.get_gateway_bot(self.token))['url']
        self._log.info(f'Try to connect to {gateway_uri}')

        if self._listener_task is not None:
            self._listener_task.cancel()
            self._listener_task = None

        if self._heartbeat_task is not None:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None
            self._last_heartbeat_ack = None

        self._listener_task = asyncio.create_task(self._web_socket_listener(gateway_uri))

        # Wait for heartbeat to start
        await asyncio.sleep(1)

        while self._last_heartbeat_ack is None:
            await asyncio.sleep(1)
            self._log.warning('Waiting on heartbeat...')

        self._log.info('Heartbeat observed, begin to identify.')

        await self._identify()

    async def _web_socket_listener(self, uri):

        async with websockets.connect(uri) as websocket:

            self._gateway_ws = websocket

            while True:

                data = await websocket.recv()
                # Dispatch to handler.
                data = json.loads(data)
                # from pprint import pprint
                # print(data)

                if 's' in data and data['s'] is not None:
                    self._sequence_number = data['s']
                    self._log.debug('Updated seq count.')

                opcode = data['op']

                if opcode == 0:
                    self._log.debug('Received event, dispatch...')
                    await self._event_dispatcher(data)

                # elif opcode == 1:
                #     # Heartbeat
                #     pass

                # elif opcode == 7:
                #     # Reconnect
                #     pass

                # elif opcode == 9:
                #     # Invalid Session
                #     pass

                elif opcode == 10:
                    # Hello
                    self._log.info('OPCODE: HELLO')
                    await self._handle_op_10(data)

                elif opcode == 11:
                    # Heartbeat ACK
                    self._log.debug('Saw a heartbeat ACK')
                    self._last_heartbeat_ack = time.time()
                    pass

                else:
                    self._log.error('Unknown opcode')
                    self._log.error(data)

    async def _heartbeat(self, interval):

        self._log.info('New heartbeat task started. Send new heartbeat NOW.')

        data = {'op': 1, 'd': self._sequence_number}
        await self._gateway_ws.send(json.dumps(data))

        while True:

            self._log.debug(f'Sleeping for {interval / 1000}s')

            await asyncio.sleep(interval / 1000)

            data = {'op': 1, 'd': self._sequence_number}
            self._log.debug(f'Sending heartbeat: {data}')

            await self._gateway_ws.send(json.dumps(data))

    async def _handle_op_10(self, data):

        if self._heartbeat_task is not None:
            self._heartbeat_task.cancel()

        self._heartbeat_task = asyncio.create_task(self._heartbeat(data['d']['heartbeat_interval']))

        self._log.debug('Opcode 10 handled.')

    async def _identify(self):
        data = {
            'op': 2,
            'd': {
                'token': self.token,
                'intents': self.intent,
                "properties": {
                    "$os": "linux",
                    "$browser": "simple_discord",
                    "$device": "simple_discord"
                }
            }
        }
        self._log.info('Sending identify.')
        await self._gateway_ws.send(json.dumps(data))

    async def _event_dispatcher(self, data):  # noqa: C901

        event_type = data['t']
        self._log.info(f'Got a {event_type}')

        if event_type == 'CHANNEL_CREATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'CHANNEL_DELETE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'CHANNEL_PINS_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'CHANNEL_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_BAN_ADD':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_BAN_REMOVE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_CREATE':
            # Cache in guild
            obj = objects.Guild()
            obj.ingest_raw_dict(data['d'])
            # pprint(data['d'])

        elif event_type == 'GUILD_DELETE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_EMOJIS_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_INTEGRATIONS_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_MEMBER_ADD':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_MEMBER_REMOVE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_MEMBER_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_ROLE_CREATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_ROLE_DELETE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_ROLE_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_STICKERS_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'INTEGRATION_CREATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'INTEGRATION_DELETE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'INTEGRATION_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'INVITE_CREATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'INVITE_DELETE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_CREATE':
            # pprint(data)
            obj = objects.Message()
            obj.ingest_raw_dict(data['d'])
            await self.on_message_create(obj, data['d'])

            # TODO: Remove this after we finish debugging interactions
            await self._debug_parse_message(obj)

        elif event_type == 'MESSAGE_DELETE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_DELETE_BULK':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_REACTION_ADD':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_REACTION_REMOVE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_REACTION_REMOVE_ALL':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_REACTION_REMOVE_EMOJI':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'PRESENCE_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'READY':
            pprint(data)

            obj = objects.Ready().from_dict(data['d'])
            self.session_id = obj.session_id
            self.ready = True
            self.me = obj.user
            self._log.info('Discord connection complete, we are ready!')
            self._log.info(f'We are now {self.me}')

            await self.on_ready(obj, data['d'])

        elif event_type == 'STAGE_INSTANCE_CREATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'STAGE_INSTANCE_DELETE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'STAGE_INSTANCE_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'THREAD_CREATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'THREAD_DELETE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'THREAD_LIST_SYNC':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'THREAD_MEMBER_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'THREAD_MEMBERS_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'THREAD_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'TYPING_START':
            # pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'VOICE_STATE_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'WEBHOOKS_UPDATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')

        elif event_type == 'INTERACTION_CREATE':
            pprint(data)
            self._log.warning(f'Encountered unhandled event {event_type}')
            interaction_id = objects.snowflake.Snowflake(data['d']['id'])
            await API.interaction_respond(
                interaction_id,
                data['d']['token'],
                {
                    'type': 4,
                    'data': {
                        'content': 'SLAP A BITCH!'
                    }
                }
            )

        else:
            # We have an unknown event on our hands, PANIC!!!
            self._log.critical(f'Encountered unknown event \'{data["t"]}\'!!!')
            pprint(data)

        # Call user wrapped cotoutines
        for user_coroutine in self._wrapper_registrations[event_type]:
            await user_coroutine(obj, data['d'])

    # Register all out events
    on_channel_create = on_channel_create
    on_channel_delete = on_channel_delete
    on_channel_pins_update = on_channel_pins_update
    on_channel_update = on_channel_update
    on_guild_ban_add = on_guild_ban_add
    on_guild_ban_remove = on_guild_ban_remove
    on_guild_create = on_guild_create
    on_guild_delete = on_guild_delete
    on_guild_emojis_update = on_guild_emojis_update
    on_guild_integrations_update = on_guild_integrations_update
    on_guild_member_add = on_guild_member_add
    on_guild_member_remove = on_guild_member_remove
    on_guild_member_update = on_guild_member_update
    on_guild_role_create = on_guild_role_create
    on_guild_role_delete = on_guild_role_delete
    on_guild_role_update = on_guild_role_update
    on_guild_stickers_update = on_guild_stickers_update
    on_guild_update = on_guild_update
    on_integration_create = on_integration_create
    on_integration_delete = on_integration_delete
    on_integration_update = on_integration_update
    on_invite_create = on_invite_create
    on_invite_delete = on_invite_delete
    on_message_create = on_message_create
    on_message_delete = on_message_delete
    on_message_delete_bulk = on_message_delete_bulk
    on_message_reaction_add = on_message_reaction_add
    on_message_reaction_remove = on_message_reaction_remove
    on_message_reaction_remove_all = on_message_reaction_remove_all
    on_message_reaction_remove_emoji = on_message_reaction_remove_emoji
    on_message_update = on_message_update
    on_presence_update = on_presence_update
    on_ready = on_ready
    on_stage_instance_create = on_stage_instance_create
    on_stage_instance_delete = on_stage_instance_delete
    on_stage_instance_update = on_stage_instance_update
    on_thread_create = on_thread_create
    on_thread_delete = on_thread_delete
    on_thread_list_sync = on_thread_list_sync
    on_thread_member_update = on_thread_member_update
    on_thread_members_update = on_thread_members_update
    on_thread_update = on_thread_update
    on_typing_start = on_typing_start
    on_voice_state_update = on_voice_state_update
    on_webhooks_update = on_webhooks_update
    on_interaction_create = on_interaction_create

    def register_handler(self, event: str):
        '''
        Register a given function to a given event string.
        '''
        if not hasattr(objects.DISCORD_EVENTS, event):
            raise ValueError(f'Attempted to bind to unknown event \'{event}\', must be exact match for existing {objects.DISCORD_EVENTS} entry.')

        def coroutine_wrapper(coroutine):
            @wraps(coroutine)
            async def wrapped_coroutine(*args, **kwargs):
                await coroutine(self, *args, **kwargs)
            self._wrapper_registrations[event].append(wrapped_coroutine)
            return wrapped_coroutine

        return coroutine_wrapper
