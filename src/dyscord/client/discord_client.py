import asyncio
import functools
import inspect
import nest_asyncio  # type: ignore
import platform
import random
import sys
import time
import warnings

from collections import defaultdict
from pprint import pprint
from typing import Any, Callable, Optional, List

import websockets
import orjson as json

from . import api, INTENTS

from .. import utilities
from .. import objects
from .. import helper

from ..version import __version__

from .events import on_any, on_channel_create, on_channel_delete, on_channel_pins_update, on_channel_update, on_guild_ban_add, on_guild_ban_remove, on_guild_create,\
    on_guild_delete, on_guild_emojis_update, on_guild_integrations_update, on_guild_member_add, on_guild_member_remove, on_guild_member_update,\
    on_guild_role_create, on_guild_role_delete, on_guild_role_update, on_guild_stickers_update, on_guild_update, on_integration_create, on_integration_delete,\
    on_integration_update, on_invite_create, on_invite_delete, on_message_create, on_message_delete, on_message_delete_bulk, on_message_reaction_add,\
    on_message_reaction_remove, on_message_reaction_remove_all, on_message_reaction_remove_emoji, on_message_update, on_presence_update, on_ready,\
    on_stage_instance_create, on_stage_instance_delete, on_stage_instance_update, on_thread_create, on_thread_delete, on_thread_list_sync,\
    on_thread_member_update, on_thread_members_update, on_thread_update, on_typing_start, on_voice_state_update, on_webhooks_update, on_interaction_create


class DiscordClient:
    '''Client for interaction with Discord.'''

    _log = utilities.Log()
    _raw_callbacks: List[Callable] = list()
    _wrapper_registrations: dict = defaultdict(lambda: list())
    _wrapper_class_registrations: list = list()
    _version = __version__
    me: objects.User
    session_id: str
    token: str
    application_id: Optional[str]
    intent: int
    ready: bool
    cache: 'utilities.Cache'

    def __init__(self, token: str, application_id: Optional[str] = None):
        '''Instantiate a DiscordClient.

        Args:
            token (str): Valid token to access discord. Only `Bot` token's currently supported.
            application_id (str): The application id. Can be left to None if client will not use Interactions.
        '''
        # Discord attributes
        DiscordClient.token = token
        DiscordClient.application_id = application_id
        DiscordClient.intent = 0
        DiscordClient.ready = False
        DiscordClient.cache = utilities.Cache()

        # Private attributes
        self._heartbeat_task = None
        self._last_heartbeat_ack = None
        self._listener_task = None
        self._sequence_number = None
        self._intents_defined = False

    def configure_intents(self,  # noqa: C901
                          guilds: bool = False,
                          guild_members: bool = False,
                          guild_bans: bool = False,
                          guild_emoji_and_stickers: bool = False,
                          guild_integrations: bool = False,
                          guild_webhooks: bool = False,
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
        '''Configure intents before connecting.

        For more details, read the [official docs](https://discord.com/developers/docs/topics/gateway#gateway-intents).

        Arguments:
            guilds (bool): Receive events related to guilds the client is a part of.
            guild_members (bool): Receive events related to guild members.
            guild_bans (bool): Receive events related to guild bans.
            guild_emoji_and_stickers (bool): Receive events related to guild emoji and stickers.
            guild_integrations (bool): Receive events related to guild Interactions.
            guild_webhooks (bool): Receive events related to guild Webhooks.
            guild_invites (bool): Receive events related to guild invites
            guild_voice_states (bool): Receive events related to guild voice states.
            guild_presences (bool): Receive events related to guild presences.
            guild_messages (bool): Receive events related to guild messages.
            guild_message_reactions (bool): Receive events related to guild reactions.
            guild_message_typeing (bool): Receive events related to guild members starting to type.
            direct_messages (bool): Receive events related to direct messages.
            direct_message_reactions (bool): Receive events related to direct message reactions.
            direct_messages_typeing (bool): Receive events related to users typing in direct messages.
        '''
        self.intent = 0
        if guilds:
            self.intent += INTENTS.GUILDS
        if guild_members:
            self.intent += INTENTS.GUILD_MEMBERS
        if guild_bans:
            self.intent += INTENTS.GUILD_BANS
        if guild_emoji_and_stickers:
            self.intent += INTENTS.GUILD_EMOJIS_AND_STICKERS
        if guild_integrations:
            self.intent += INTENTS.GUILD_INTEGRATIONS
        if guild_webhooks:
            self.intent += INTENTS.GUILD_WEBHOOKS
        if guild_invites:
            self.intent += INTENTS.GUILD_INVITES
        if guild_voice_states:
            self.intent += INTENTS.GUILD_VOICE_STATES
        if guild_presences:
            self.intent += INTENTS.GUILD_PRESENCES
        if guild_messages:
            self.intent += INTENTS.GUILD_MESSAGES
        if guild_message_reactions:
            self.intent += INTENTS.GUILD_MESSAGE_REACTIONS
        if guild_message_typeing:
            self.intent += INTENTS.GUILD_MESSAGE_TYPING
        if direct_messages:
            self.intent += INTENTS.DIRECT_MESSAGES
        if direct_message_reactions:
            self.intent += INTENTS.DIRECT_MESSAGE_REACTIONS
        if direct_messages_typeing:
            self.intent += INTENTS.DIRECT_MESSAGE_TYPING
        self._intents_defined = True

    def set_all_intents(self):
        '''Set all intents to True. For more information see the configure_intents() function.'''
        self.intent = 0
        for intent in INTENTS:
            self.intent += intent
        self._intents_defined = True

    def run(self, loop: asyncio.AbstractEventLoop = None):
        '''Start the async loop and run forever.

        Arguments:
            loop (asyncio.AbstractEventLoop): If desired, use a given asyncio compatible loop. One will be created if not given.
        '''
        self._log.info('Starting...')
        self._log.info(f'Platform: [{platform.platform()}]')
        self._log.info(f'Python Version: [{sys.version}]')
        self._log.info(f'Python Version Info: [{sys.version_info}]')
        self._log.info(f'Dyscord Version: [v{__version__}]')

        loop = loop if loop is not None else asyncio.get_event_loop()

        nest_asyncio.apply(loop)

        loop.create_task(self._run())

        loop.run_forever()

    async def _run(self, ):

        if self._intents_defined is False:
            warnings.warn('Started without defining intents. Client will likely get ZERO input. Consider calling the \'configure_intents\' function.', UserWarning)

        # BUG: This might cause Runtime errors, we need to wait and see. See https://github.com/erdewit/nest_asyncio/issues/22.
        # This will be left here for now, as it avoids weird issues and allows us to work if the user bypasses run().
        nest_asyncio.apply()

        loop = asyncio.get_event_loop()
        if not hasattr(loop, '_nest_patched'):
            raise RuntimeError('Cannot run this library without running \'nest_asyncio.apply()\' first.')

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
        '''TODO: Implement connection to discord's servers.'''
        api.API.TOKEN = self.token
        if type(self.application_id) is str:
            api.API.APPLICATION_ID = self.application_id

        gateway_uri = (await api.API.get_gateway_bot(self.token))['url']
        self._log.debug(f'Try to connect to {gateway_uri}')

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

        self._log.debug('Heartbeat observed, begin to identify.')

        await self._identify()

    async def _web_socket_listener(self, uri):  # noqa

        def _handle_completed_tasks(task: asyncio.Task):
            exception = task.exception()
            if exception is None:
                return
            try:
                raise exception
            except Exception:
                self._log.exception('Exception from event dispatcher.')

        async with websockets.connect(uri) as websocket:

            self._gateway_ws = websocket

            while True:

                data = await websocket.recv()
                data = json.loads(data)

                for callback in self._raw_callbacks:
                    await callback(data)

                if 's' in data and data['s'] is not None:
                    self._sequence_number = data['s']
                    self._log.debug('Updated seq count to [{self._sequence_number}].')

                opcode = data['op']

                if opcode == 0:
                    self._log.debug('Received event, dispatch...')
                    task = asyncio.create_task(self._event_dispatcher(data))
                    task.add_done_callback(_handle_completed_tasks)

                elif opcode == 1:
                    self._log.debug('OPCODE: HEARTBEAT')
                    data = {'op': 1, 'd': self._sequence_number}
                    await self._gateway_ws.send(json.dumps(data))

                elif opcode == 7:
                    self._log.debug('OPCODE: RECONNECT')
                    await self._handle_op_7(data)

                elif opcode == 9:
                    self._log.debug('OPCODE: INVALID SESSION')
                    await self._handle_op_9(data)

                elif opcode == 10:
                    # Hello
                    self._log.debug('OPCODE: HELLO')
                    await self._handle_op_10(data)

                elif opcode == 11:
                    self._log.debug('Saw a heartbeat ACK')
                    self._last_heartbeat_ack = time.time()

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

    async def _handle_op_7(self, data):

        await self._reconnect()

        self._log.critical('Opcode 7 handled.')

    async def _handle_op_9(self, data):

        if self._listener_task is not None:
            self._listener_task.cancel()
            self._listener_task = None

        if self._heartbeat_task is not None:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None
            self._last_heartbeat_ack = None
            self._gateway_ws = None

        # Wait 1-5 seconds then try to connect.
        await asyncio.sleep(random.random() * 4 + 1)

        await self._reconnect()

        self._log.critical('Opcode 9 handled.')

    async def _handle_op_10(self, data):

        if self._heartbeat_task is not None:
            self._heartbeat_task.cancel()

        self._heartbeat_task = asyncio.create_task(self._heartbeat(data['d']['heartbeat_interval']))

        self._log.debug('Opcode 10 handled.')

    async def _reconnect(self):
        '''Send a reconnect message.'''
        gateway_uri = (await api.API.get_gateway_bot(self.token))['url']
        self._log.critical(f'Try to connect to {gateway_uri}')

        if self._listener_task is not None:
            self._listener_task.cancel()
            self._listener_task = None

        if self._heartbeat_task is not None:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None
            self._last_heartbeat_ack = None
            self._gateway_ws = None

        self._listener_task = asyncio.create_task(self._web_socket_listener(gateway_uri))

        while self._gateway_ws is None:
            await asyncio.sleep(1)

        data = {
            'op': 6,
            'd': {
                'token': self.token,
                'session_id': self.session_id,
                'seq': self._sequence_number,
            }
        }
        self._log.info('Sending reconnect.')
        await self._gateway_ws.send(json.dumps(data))

    async def _identify(self):
        data = {
            'op': 2,
            'd': {
                'token': self.token,
                'intents': self.intent,
                "properties": {
                    "$os": "linux",
                    "$browser": "dyscord",
                    "$device": "dyscord"
                }
            }
        }
        self._log.info('Sending identify.')
        await self._gateway_ws.send(json.dumps(data))

    async def _event_dispatcher(self, data):  # noqa: C901

        event_type = data['t']
        self._log.info(f'Got a {event_type}')
        obj = None

        # pprint(data)

        if event_type == 'READY':
            obj = objects.Ready().from_dict(data['d'])
            DiscordClient.session_id = obj.session_id
            DiscordClient.ready = True
            DiscordClient.me = obj.user
            self._log.info('Discord connection complete, we are ready!')
            self._log.info(f'We are now {self.me}')

        elif not DiscordClient.ready:
            self._log.info(f'Got event of type [{event_type}] before we were ready!')
            return

        elif event_type == 'CHANNEL_CREATE':
            obj = objects.ChannelImporter().from_dict(data['d'])

        elif event_type == 'CHANNEL_DELETE':
            obj = objects.ChannelImporter().from_dict(data['d'])

        elif event_type == 'CHANNEL_PINS_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'CHANNEL_UPDATE':
            obj = objects.ChannelImporter().from_dict(data['d'])

        elif event_type == 'GUILD_BAN_ADD':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_BAN_REMOVE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_CREATE':
            obj = objects.Guild().from_dict(data['d'])

        elif event_type == 'GUILD_DELETE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_EMOJIS_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_INTEGRATIONS_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_MEMBER_ADD':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_MEMBER_REMOVE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_MEMBER_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_ROLE_CREATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_ROLE_DELETE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_ROLE_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_STICKERS_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'GUILD_UPDATE':
            obj = objects.Guild().from_dict(data['d'])

        elif event_type == 'INTEGRATION_CREATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'INTEGRATION_DELETE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'INTEGRATION_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'INVITE_CREATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'INVITE_DELETE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_CREATE':
            obj = objects.Message().from_dict(data['d'])

        elif event_type == 'MESSAGE_DELETE':
            obj = objects.Message().from_dict(data['d'])

        elif event_type == 'MESSAGE_DELETE_BULK':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_REACTION_ADD':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_REACTION_REMOVE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_REACTION_REMOVE_ALL':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_REACTION_REMOVE_EMOJI':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'MESSAGE_UPDATE':
            obj = objects.Message().from_dict(data['d'])

        elif event_type == 'PRESENCE_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'STAGE_INSTANCE_CREATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'STAGE_INSTANCE_DELETE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'STAGE_INSTANCE_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'THREAD_CREATE':
            pprint(data)
            obj = objects.ChannelImporter().from_dict(data['d'])

        elif event_type == 'THREAD_DELETE':
            obj = objects.ChannelImporter().from_dict(data['d'])

        elif event_type == 'THREAD_LIST_SYNC':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'THREAD_MEMBER_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'THREAD_MEMBERS_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'THREAD_UPDATE':
            obj = objects.ChannelImporter().from_dict(data['d'])

        elif event_type == 'TYPING_START':
            obj = objects.events.typing_start.TypingStart().from_dict(data['d'])

        elif event_type == 'VOICE_STATE_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'WEBHOOKS_UPDATE':
            warnings.warn(f'Encountered unhandled event {event_type}')

        elif event_type == 'INTERACTION_CREATE':
            obj = objects.interactions.Interaction().from_dict(data['d'])
            self._log.info('Saw INTERACTION_CREATE event.')
            await helper.CommandHandler.command_handler(self, obj)

        else:
            # We have an unknown event on our hands, PANIC!!!
            self._log.critical(f'Encountered unknown event \'{data["t"]}\'!!!')
            pprint(data)
            return

        event_handler_name = f'on_{event_type.lower()}'

        # Call own event handlers first.
        if hasattr(self, event_handler_name):
            self_function = getattr(self, event_handler_name)
            await self_function(obj, data)

        # Call user wrapped classes, functions and cotoutines.
        # TODO: Should we invoke a create_task when able to avoid blocking calls?
        arguments = (obj, data, self)
        if obj is not None:
            for user_function in DiscordClient._wrapper_registrations[event_type]:
                arg_len = len(inspect.signature(user_function).parameters)
                assert arg_len >= 0 and arg_len <= 3
                if asyncio.iscoroutinefunction(user_function):
                    await user_function(*arguments[:arg_len])
                else:
                    user_function(*arguments[:arg_len])

            for user_class in DiscordClient._wrapper_class_registrations:
                if hasattr(user_class, event_handler_name):
                    user_function = getattr(user_class, event_handler_name)
                    arg_len = len(inspect.signature(user_function).parameters)
                    assert arg_len >= 0 and arg_len <= 4
                    if list(inspect.signature(user_function).parameters.items())[0][0] != 'cls':
                        warnings.warn('Wrapped class does not appear to be using class methods, unexpected behavior may result!', UserWarning)
                    if asyncio.iscoroutinefunction(user_function):
                        await user_function(user_class, *arguments[:arg_len])
                    else:
                        user_function(user_class, *arguments[:arg_len])

        # Handle the special case of the ANY event.
        for user_function in DiscordClient._wrapper_registrations['ANY']:
            arg_len = len(inspect.signature(user_function).parameters)
            assert arg_len >= 0 and arg_len <= 3
            if asyncio.iscoroutinefunction(user_function):
                await user_function(*arguments[:arg_len])
            else:
                user_function(*arguments[:arg_len])

        for user_class in DiscordClient._wrapper_class_registrations:
            if hasattr(user_class, 'on_any'):
                user_function = getattr(user_class, event_handler_name)
                arg_len = len(inspect.signature(user_function).parameters)
                assert arg_len >= 0 and arg_len <= 4
                if list(inspect.signature(user_function).parameters.items())[0][0] != 'cls':
                    warnings.warn('Wrapped class does not appear to be using class methods, unexpected behavior may result!', UserWarning)

                if asyncio.iscoroutinefunction(user_function):
                    await user_function(user_class, *arguments[:arg_len])
                else:
                    user_function(user_class, *arguments[:arg_len])

    # Register all out events
    on_any = on_any
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

    @classmethod
    def decorate_handler(cls, event: str):
        '''Register a given function to a given event string.

        This function should be used as a decorator around a function to map that function to a given event. The decorator takes one argument, a string which maps to the type of event we should map
        to. See the definition of DISCORD_EVENTS for names to map against.

        The decorated mapped should by an `async` function, although synchronous functions are allowed (and highly discouraged).

        The arguments of the decorated decide which python objects are given to the function when the given event is called. The mapping is as follows:

        - 1 Argument -> (discord_object)
        - 2 Argument -> (discord_object, raw_dict)
        - 3 Argument -> (discord_object, raw_dict, client)

        The `discord_object` will be a python representation of the event object.

        The `raw_dict` is a raw dictionary the API emitted.

        The `client` is the DiscordClient instance.
        '''
        if not hasattr(objects.DISCORD_EVENTS, event) and event != 'ANY':
            raise ValueError(f'Attempted to bind to unknown event \'{event}\', must be exact match for existing {objects.DISCORD_EVENTS} entry.')

        def func_wrapper(func):
            arg_len = len(inspect.signature(func).parameters)
            assert arg_len >= 0 and arg_len <= 3
            if asyncio.iscoroutinefunction(func):
                @functools.wraps(func)
                async def wrapped_func(*args, **kwargs):  # type: ignore
                    await func(*args, **kwargs)

                cls._wrapper_registrations[event].append(wrapped_func)
                return wrapped_func
            else:
                @functools.wraps(func)
                def wrapped_func(*args, **kwargs):  # type: ignore
                    func(*args, **kwargs)

                cls._wrapper_registrations[event].append(wrapped_func)
                return wrapped_func

        return func_wrapper

    @classmethod
    def decorate_class(cls, target_class):
        '''Register a given class and attempt to call any valid on_<event> functions.

        By convention functions of the class should be async.
        '''

        @functools.wraps(target_class)
        async def class_wrapper(cls, *args, **kwargs):
            pass

        cls._wrapper_class_registrations.append(class_wrapper)

        return class_wrapper

    @classmethod
    def _register_raw_callback(cls, callback: Callable[[dict], Any]):
        '''Register a raw callback that will receive pure dicts from the API.'''
        cls._raw_callbacks.append(callback)
