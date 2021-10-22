import asyncio
from collections import defaultdict
from typing import Any, Optional, Union, List, Dict

from ...client import api

from ..base_object import BaseDiscordObject

from .. import channel
from .. import snowflake

from .. import user as ext_user, message as ext_message, embed as ext_embed, role

from . import enumerations, components as ext_components, command


class InteractionStructure(BaseDiscordObject):
    '''Response given from the server after an user activated an interaction of some type.'''

    INTERACTION_RESPONSE_TYPES = enumerations.INTERACTION_RESPONSE_TYPES

    id: snowflake.Snowflake
    application_id: snowflake.Snowflake
    type: enumerations.INTERACTION_TYPES
    data: Optional['InteractionDataStructure']
    guild_id: Optional[snowflake.Snowflake]
    # TODO: add a Guild object from the ID.
    channel_id: Optional[snowflake.Snowflake]
    # TODO: add a Channel object from the ID.
    member: Optional['ext_user.Member']
    user: Optional['ext_user.User']
    token: str
    version: int
    message: Optional['ext_message.Message']

    def __init__(self):
        '''Simple initialization.'''
        self._response_generated = False
        self.id = None

    @property
    def can_respond(self):
        '''Determine if you can respond to this interaction.'''
        # TODO: We could check timestamps here as well!
        return self._response_generated is False

    @property
    def can_followup(self):
        '''Determine if you can followup to this interaction.'''
        # TODO: We could check timestamps here as well!
        return self._response_generated is True

    def from_dict(self, data: dict) -> 'InteractionStructure':
        '''Import data from dict and populate object with it.'''
        self._log.info('Parsing  a InteractionStructure dict')
        self.application_id = snowflake.Snowflake(data['application_id'])
        self.id = snowflake.Snowflake(data['id'])
        self.token = str(data['token'])
        self.version = int(data['version'])
        self.type = enumerations.INTERACTION_TYPES(data['type'])
        if 'channel_id' in data:
            self.channel_id = snowflake.Snowflake(data['channel_id'])
        if 'guild_id' in data:
            self.guild_id = snowflake.Snowflake(data['guild_id'])
        if 'data' in data:
            guild_id = data['guild_id'] if 'guild_id' in data else None
            self.data = InteractionDataStructure().from_dict(data['data'], guild_id)
        if 'channel_id' in data:
            self.channel_id = snowflake.Snowflake(data['channel_id'])
        if 'user' in data:
            self.user = ext_user.User().from_dict(data['user'])
        if 'member' in data:
            self.member = ext_user.Member().from_dict(data['member'])
        if 'message' in data:
            self.message = ext_message.Message().from_dict(data['message'])

        return self

    def generate_response(self,
                          type: enumerations.INTERACTION_RESPONSE_TYPES = enumerations.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE,
                          ephemeral: bool = False,
                          ) -> 'InteractionResponse':
        '''Produce a InteractionResponse object to follow up against the InteractionStructure.'''
        if self._response_generated:
            raise RuntimeError('You cannot reuse a token from a response. Call generate_followup()')
        else:
            self._response_generated = True
        new_response = InteractionResponse()
        new_response.interaction_id = self.id
        new_response.interaction_token = self.token
        new_response.type = type
        if ephemeral:
            new_response.data.flags |= enumerations.INTERACTION_CALLBACK_FLAGS.EPHEMERAL
        return new_response

    def generate_followup(self,
                          ephemeral: bool = False,
                          ) -> 'InteractionFollowup':
        '''Produce a InteractionFollowup object to follow up against the InteractionStructure.'''
        if self._response_generated is False:
            raise RuntimeError('You cannot followup on an interaction until you respond to it. Call generate_response()')
        new_followup = InteractionFollowup()
        new_followup.interaction_id = self.id
        new_followup.interaction_token = self.token
        if ephemeral:
            new_followup.data.flags |= enumerations.INTERACTION_CALLBACK_FLAGS.EPHEMERAL

        return new_followup


class InteractionDataStructure(BaseDiscordObject):
    '''Handle data from an InteractionStructure.'''

    id: snowflake.Snowflake  # snowflake the ID of the invoked command Application Command
    name: str  # string the name of the invoked command Application Command
    type: enumerations.COMMAND_TYPE  # integer the type of the invoked command Application Command
    resolved: Dict[str, dict]  # ? resolved data converted users + roles + channels Application Command
    options: Dict[str, Any]  # ? array of application command interaction data option the params + values from the user Application Command
    custom_id: str  # ? string the custom_id of the component Component
    component_type: Optional[enumerations.COMPONENT_TYPES]  # ? integer the type of the component Component
    values: Optional[List['command.CommandOptions']]  # ? array of select option values the values the user selected Component (Select)
    target_id: Optional[snowflake.Snowflake]  # ? snowflake id the of user or message targetted by a user or message command

    def from_dict(self, data: dict, guild_id: Optional['snowflake.Snowflake'] = None) -> 'InteractionDataStructure':  # noqa: C901
        '''Import data from dict and populate object with it.'''
        self._log.info('Parse a InteractionDataStructure dict.')
        if 'id' in data:
            self.id = snowflake.Snowflake(data['id'])
        if 'name' in data:
            self.name = data['name']
        if 'type' in data:
            self.type = enumerations.COMMAND_TYPE(data['type'])
        if 'resolved' in data:
            self._log.info('FOUND RESOLVED!')
            self.resolved = defaultdict(lambda: dict())
            for resolution_type in data['resolved']:
                self._log.info(f'Resolved [{resolution_type}].')
                for entry_id in data['resolved'][resolution_type]:
                    if resolution_type == 'members':
                        self.resolved[resolution_type][entry_id] = ext_user.Member()
                    elif resolution_type == 'users':
                        self.resolved[resolution_type][entry_id] = ext_user.User()
                    elif resolution_type == 'messages':
                        self.resolved[resolution_type][entry_id] = ext_message.Message()
                    elif resolution_type == 'channels':
                        self.resolved[resolution_type][entry_id] = channel.ChannelImporter()
                    elif resolution_type == 'roles':
                        self.resolved[resolution_type][entry_id] = role.Role()
                    else:
                        self._log.critical(f'Cannot resolve type [{resolution_type}]!')
                        raise TypeError

                    self.resolved[resolution_type][entry_id].from_dict(data['resolved'][resolution_type][entry_id])
        if 'component_type' in data:
            self.component_type = enumerations.COMPONENT_TYPES(data['component_type'])
        if 'custom_id' in data:
            self.custom_id = str(data['custom_id'])
        if 'target_id' in data:
            self.target_id = snowflake.Snowflake(data['target_id'])

        self.options = dict()
        if 'options' in data:
            for option_dict in data['options']:
                self.options[option_dict['name']] = InteractionDataOptionStructure().from_dict(option_dict, guild_id).parse(guild_id)
        return self


class InteractionDataOptionStructure(BaseDiscordObject):
    '''InteractionDataOptionStructure.'''

    name: str                                                  # string the name of the invoked command Application Command
    type: enumerations.COMMAND_OPTION                          # integer the type of the invoked command Application Command
    value: Optional[Union[str, int, bool, 'snowflake.Snowflake', float]]               # the value of the pair
    options: Optional[Dict[str, Any]]  # Present when command is a group or subcommand

    def __getitem__(self, key: str):
        '''Return item from the options dict.'''
        if hasattr(self, 'options') and type(self.options) is dict:
            return self.options[key]

    def __contains__(self, item: str):
        '''Determine if item is in the options dict.'''
        if hasattr(self, 'options') and type(self.options) is dict:
            return item in self.options

    def from_dict(self, data: dict, guild_id: Optional['snowflake.Snowflake'] = None) -> 'InteractionDataOptionStructure':  # noqa: C901
        '''Import data from dict and populate object with it.'''
        self.name = data['name']
        self.type = enumerations.COMMAND_OPTION(data['type'])
        if 'value' in data:
            if self.type == enumerations.COMMAND_OPTION.SUB_COMMAND:
                raise ValueError('Sub Commands should not have values!')
            elif self.type == enumerations.COMMAND_OPTION.SUB_COMMAND_GROUP:
                raise ValueError('Sub Command Groups should not have values!')
            elif self.type in [enumerations.COMMAND_OPTION.STRING, enumerations.COMMAND_OPTION.INTEGER, enumerations.COMMAND_OPTION.BOOLEAN, enumerations.COMMAND_OPTION.NUMBER]:
                self.value = data['value']
            elif self.type == enumerations.COMMAND_OPTION.USER:
                # TODO: Actually lookup the user here and replace the snowflake with a full object.
                self.value = snowflake.Snowflake(data['value'])
            elif self.type == enumerations.COMMAND_OPTION.CHANNEL:
                # TODO: Actually lookup the channel here and replace the snowflake with a full object.
                self.value = snowflake.Snowflake(data['value'])
            elif self.type == enumerations.COMMAND_OPTION.ROLE:
                # TODO: Actually lookup the role here and replace the snowflake with a full object.
                self.value = snowflake.Snowflake(data['value'])
            elif self.type == enumerations.COMMAND_OPTION.MENTIONABLE:
                # TODO: Actually lookup the mentionable here and replace the snowflake with a full object.
                self.value = snowflake.Snowflake(data['value'])
        self.options = dict()
        if 'options' in data:
            for option_dict in data['options']:
                self.options[option_dict['name']] = InteractionDataOptionStructure().from_dict(option_dict, guild_id).parse(guild_id)
        return self

    def parse(self, guild_id: Optional['snowflake.Snowflake'] = None):  # noqa: C901
        '''Look at the type field of self and attempt to return a sane result.

        For SUB_COMMAND and SUB_COMMAND_GROUP types, return another InteractionDataOptionStructure object.
        For all others, attempt to reference the type and handle it.
        '''
        CO = enumerations.COMMAND_OPTION

        if self.type in [CO.SUB_COMMAND, CO.SUB_COMMAND_GROUP]:
            return self

        if self.type in [CO.STRING, CO.INTEGER, CO.BOOLEAN, CO.NUMBER]:
            return self.value

        assert type(self.value) is snowflake.Snowflake

        if self.type == CO.USER:
            return ext_user.User().from_dict(asyncio.run(api.API.get_user(self.value)))

        if self.type == CO.CHANNEL:
            return channel.Channel().from_dict(asyncio.run(api.API.get_channel(self.value)))

        if self.type == CO.ROLE:
            assert type(guild_id) is snowflake.Snowflake
            roles_list = asyncio.run(api.API.get_guild_roles(guild_id))
            for role_dict in roles_list:
                if role_dict['id'] == self.value:
                    return role.Role().from_dict(role_dict)

        if self.type == CO.MENTIONABLE:
            try:
                return ext_user.User().from_dict(asyncio.run(api.API.get_user(self.value)))
            except Exception:
                assert type(guild_id) is snowflake.Snowflake
                roles_list = asyncio.run(api.API.get_guild_roles(guild_id))
                for role_dict in roles_list:
                    if role_dict['id'] == self.value:
                        return role.Role().from_dict(role_dict)


class InteractionResponse(BaseDiscordObject):
    '''Manage a response message to an interaction.'''

    INTERACTION_RESPONSE_TYPES = enumerations.INTERACTION_RESPONSE_TYPES

    type: enumerations.INTERACTION_RESPONSE_TYPES
    data: 'InteractionCallback'

    # The following are part of our local book keeping, not the discord structure.
    interaction_id: 'snowflake.Snowflake'
    interaction_token: str

    def __init__(self):
        '''Initialize InteractionResponse.'''
        self.data = InteractionCallback()
        self.last_followup_message: Optional['ext_message.Message'] = None

    def to_dict(self) -> dict:
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()
        new_dict['type'] = self.type.value
        new_dict['data'] = self.data.to_dict()
        return new_dict

    async def send(self) -> None:
        '''Send response.'''
        await api.API.create_interaction_response(self.interaction_id, self.interaction_token, self.to_dict())

    async def edit_original_response(self):
        '''Edit the initial response to the original interaction.'''
        data = await self._generate_webhook_data()
        await api.API.edit_original_interaction_response(self.interaction_token, data)

    async def delete_initial_response(self):
        '''Delete the initial response to the original interaction.'''
        await api.API.delete_original_interaction_response(self.interaction_token)

    def generate(self,
                 content: Optional[str] = None,
                 tts: Optional[bool] = None,
                 ephemeral: bool = False,
                 ):
        '''Passthrough to data generate function.'''
        return self.data.generate(tts, content, ephemeral)

    def add_components(self) -> 'ext_components.ActionRow':
        '''Add component objects to the data attribute.'''
        return self.data.add_components()

    def add_embeds(self) -> 'ext_embed.Embed':
        '''Add embed objects to the data attribute.'''
        return self.data.add_embeds()


class InteractionFollowup(BaseDiscordObject):
    '''Manage a followup message to an interaction.'''

    data: 'InteractionCallback'

    # The following are part of our local book keeping, not the discord structure.
    interaction_id: 'snowflake.Snowflake'
    interaction_token: str

    def __init__(self):
        '''Initialize InteractionFollowup.'''
        self.data = InteractionCallback()
        self.last_followup_message: Optional['ext_message.Message'] = None

    def to_dict(self) -> dict:
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()
        new_dict['data'] = self.data.to_dict()
        return new_dict

    async def send(self) -> 'ext_message.Message':
        '''Send followup.'''
        # TODO: We can do some cool stuff with overrides here, look into that. https://discord.com/developers/docs/resources/webhook#execute-webhook
        data = await self._generate_webhook_data()
        msg_dict = await api.API.create_followup_message(self.interaction_token, data)
        new_message = ext_message.Message().from_dict(msg_dict)
        self.last_followup_message = new_message
        return new_message

    async def edit_original_response(self):
        '''Edit the initial response to the original interaction.'''
        data = await self._generate_webhook_data()
        await api.API.edit_original_interaction_response(self.interaction_token, data)

    async def delete_initial_response(self):
        '''Delete the initial response to the original interaction.'''
        await api.API.delete_original_interaction_response(self.interaction_token)

    async def edit_followup_message(self, message: Optional['ext_message.Message'] = None) -> 'ext_message.Message':
        '''Apply modifications to the given message object.'''
        # TODO: We can do some cool stuff with overrides here, look into that. https://discord.com/developers/docs/resources/webhook#execute-webhook
        data = await self._generate_webhook_data()
        if message is None:
            if self.last_followup_message is not None:
                message = self.last_followup_message
            else:
                raise ValueError('Must give specific followup message, or have sent one already.')
        msg_dict = await api.API.edit_followup_message(self.interaction_token, message.id, data)
        new_message = ext_message.Message().from_dict(msg_dict)
        self.last_followup_message = new_message
        return new_message

    async def delete_followup_message(self, message: Optional['ext_message.Message'] = None) -> None:
        '''Delete the given followup message.

        If a message was just send using the send() method of this object, and no message argument is given, then attempt to delete the last followup message.
        '''
        if message is None:
            if self.last_followup_message is not None:
                message = self.last_followup_message
            else:
                raise ValueError('Must give specific followup message, or have sent one already.')
        await api.API.delete_followup_message(self.interaction_token, message.id)

    async def _generate_webhook_data(self) -> dict:
        data_structure: dict = dict()
        if hasattr(self.data, 'content'):
            data_structure['content'] = self.data.content
        if hasattr(self.data, 'embeds'):
            data_structure['embeds'] = list()
            assert type(self.data.embeds) is list
            for embed in self.data.embeds:
                data_structure['embeds'].append(embed.to_dict())
        if hasattr(self.data, 'components'):
            data_structure['components'] = list()
            assert type(self.data.components) is list
            for component in self.data.components:
                data_structure['components'].append(component.to_dict())
        return data_structure

    def generate(self,
                 content: Optional[str] = None,
                 tts: Optional[bool] = None,
                 ephemeral: bool = False,
                 ):
        '''Passthrough to data generate function.'''
        return self.data.generate(tts, content, ephemeral)

    def add_components(self) -> 'ext_components.ActionRow':
        '''Add components objects to the data attribute.'''
        return self.data.add_components()

    def add_embeds(self) -> 'ext_embed.Embed':
        '''Add embed objects to the data attribute.'''
        return self.data.add_embeds()


class InteractionCallback(BaseDiscordObject, ext_components.ComponentAdder, ext_embed.EmbedAdder):
    '''InteractionCallback.'''

    INTERACTION_CALLBACK_FLAGS = enumerations.INTERACTION_CALLBACK_FLAGS

    tts: Optional[bool]
    content: Optional[str]
    embeds: Optional[List['ext_embed.Embed']]  # TODO: Support embeds here.
    # allowed_mentions: dict
    flags: int
    components: Optional[List[ext_components.Component]]

    def __init__(self):
        '''InteractionCallback.'''
        self.flags = 0
        self.embeds = list()
        self.components = list()

    def to_dict(self) -> dict:
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()
        new_dict['flags'] = self.flags
        if hasattr(self, 'tts'):
            new_dict['tts'] = self.tts
        if hasattr(self, 'content'):
            new_dict['content'] = self.content
        if hasattr(self, 'components'):
            new_dict['components'] = list()
            assert type(self.components) is list
            assert type(new_dict['components']) is list
            for component in self.components:
                new_dict['components'].append(component.to_dict())
        if hasattr(self, 'embeds'):
            new_dict['embeds'] = list()
            assert type(self.embeds) is list
            assert type(new_dict['embeds']) is list
            for embed in self.embeds:
                new_dict['embeds'].append(embed.to_dict())
        return new_dict

    def generate(self,
                 tts: Optional[bool] = None,
                 content: Optional[str] = None,
                 ephemeral: bool = False,
                 ):
        '''Customize common attributes of a callback.

        Arguments:
            tts (bool): Send message as text to speech.
            content (str): Text contents of the message to send.
            ephemeral (bool): Only show message to the target user, default is `False`.
        '''
        if tts is not None:
            self.tts = tts
        if content is not None:
            self.content = content
        self.flags = 0
        if ephemeral:
            self.flags |= self.INTERACTION_CALLBACK_FLAGS.EPHEMERAL
        self.components = []
