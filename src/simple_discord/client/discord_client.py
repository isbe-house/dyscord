import asyncio
import time
from pprint import pprint
from typing import Optional

import websockets
import orjson as json

from .api import API
from .gateway_intents import Intents


from .. import utilities
from .. import objects


class DiscordClient:

    _log = utilities.Log()

    def __init__(self, token: str, application_id: Optional[str] = None):
        self.token = token
        self.application_id = application_id
        self.intent = 0
        self.ready = False
        self.session_id: str
        self.cache = utilities.Cache()
        self.me: objects.User

        self._heartbeat_task = None
        self._last_heartbeat_ack = None
        self._listener_task = None
        self._sequence_number = None

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
            self.session_id = data['d']['session_id']
            self.ready = True
            self.me = objects.User().from_dict(data['d']['user'])
            self._log.info('Discord connection complete, we are ready!')
            self._log.info(f'We are now {self.me}')

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

    async def _debug_parse_message(self, message):
        if self.me in message.mentions:
            self._log.info(f'Saw message: {message.content}')
            if 'PURGE' in message.content:
                self._log.critical('Purging all commands.')
                await self._purge_commands()
            elif 'REGISTER' in message.content:
                self._log.critical('Registering test commands.')
                await self._register_commands()

    async def _purge_commands(self):
        from pprint import pprint
        self._log.info('Get global commands')
        commands = await API.get_global_application_commands()
        for command in commands:
            command = objects.interactions.CommandStructure().from_dict(command)
            pprint(commands)
            assert command.id is not None
            await API.delete_global_application_command(command.id)

        self._log.info('Get guild commands')
        for guild in utilities.Cache().guilds:
            pprint(guild)
            commands = await API.get_guild_application_commands(guild.id)
            for command in commands:
                command = objects.interactions.CommandStructure().from_dict(command)
                pprint(command)
                assert command.id is not None
                await API.delete_guild_application_command(guild.id, command.id)

    async def _register_commands(self):
        new_command = objects.interactions.CommandStructure()
        new_command.generate(
            name='test2',
            description='This is a more complex test.',
            type=new_command.COMMAND_TYPE.CHAT_INPUT,
        )
        new_command.add_option_typed(
            type=objects.interactions.CommandOptions.COMMAND_OPTION.BOOLEAN,
            name='hit_them',
            description='Age of the target',
        )
        new_command.validate()
        data = new_command.to_dict()

        await API.create_global_application_command(data)