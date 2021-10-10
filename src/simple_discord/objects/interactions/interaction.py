from collections import defaultdict
from typing import Optional, Union, List, Dict

from ...client import api

from ..base_object import BaseDiscordObject

from .. import snowflake

from .. import user as ext_user, message as ext_message

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

    def from_dict(self, data: dict) -> 'InteractionStructure':
        self._log.info('Parsing  a InteractionStructure dict')
        self.application_id = snowflake.Snowflake(data['application_id'])
        self.id = snowflake.Snowflake(data['id'])
        self.token = str(data['token'])
        self.version = int(data['version'])
        self.type = enumerations.INTERACTION_TYPES(data['type'])
        if 'channel_id' in data:
            self.channel_id = snowflake.Snowflake(data['channel_id'])
        if 'data' in data:
            self.data = InteractionDataStructure().from_dict(data['data'])
        if 'guild_id' in data:
            self.guild_id = snowflake.Snowflake(data['guild_id'])
        if 'channel_id' in data:
            self.channel_id = snowflake.Snowflake(data['channel_id'])
        if 'user' in data:
            self.user = ext_user.User().from_dict(data['user'])
        if 'member' in data:
            self.member = ext_user.Member().from_dict(data['member'])

        return self

    def generate_response(self,
                          ephemeral: bool = False,
                          type: enumerations.INTERACTION_RESPONSE_TYPES = enumerations.INTERACTION_RESPONSE_TYPES.CHANNEL_MESSAGE_WITH_SOURCE,
                          ) -> 'InteractionResponse':
        new_response = InteractionResponse()
        new_response.interaction_id = self.id
        new_response.interaction_token = self.token
        new_response.type = type
        if ephemeral:
            new_response.data.flags |= enumerations.INTERACTION_CALLBACK_FLAGS.EPHEMERAL
        return new_response


class InteractionDataStructure(BaseDiscordObject):
    id: snowflake.Snowflake  # snowflake the ID of the invoked command Application Command
    name: str  # string the name of the invoked command Application Command
    type: enumerations.COMMAND_TYPE  # integer the type of the invoked command Application Command
    resolved: Dict[str, dict]  # ? resolved data converted users + roles + channels Application Command
    options: List  # ? array of application command interaction data option the params + values from the user Application Command
    custom_id: str  # ? string the custom_id of the component Component
    component_type: Optional[enumerations.COMPONENT_TYPES]  # ? integer the type of the component Component
    values: Optional[List['command.CommandOptions']]  # ? array of select option values the values the user selected Component (Select)
    target_id: Optional[snowflake.Snowflake]  # ? snowflake id the of user or message targetted by a user or message command

    def from_dict(self, data: dict) -> 'InteractionDataStructure':  # noqa: C901
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
                    self.resolved[resolution_type][entry_id].from_dict(data['resolved'][resolution_type][entry_id])
        if 'component_type' in data:
            self.component_type = enumerations.COMPONENT_TYPES(data['component_type'])
        if 'custom_id' in data:
            self.custom_id = str(data['custom_id'])
        if 'target_id' in data:
            self.target_id = snowflake.Snowflake(data['target_id'])
        if 'options' in data:
            self.options = list()
            for option_dict in data['options']:
                self.options.append(InteractionDataOptionStructure().from_dict(option_dict))
        return self


class InteractionDataOptionStructure(BaseDiscordObject):

    name: str                                                  # string the name of the invoked command Application Command
    type: enumerations.COMMAND_OPTION                          # integer the type of the invoked command Application Command
    value: Optional[Union[str, int, bool, 'snowflake.Snowflake', float]]               # the value of the pair
    options: Optional[List['InteractionDataOptionStructure']]  # Present when command is a group or subcommand

    def from_dict(self, data: dict) -> 'InteractionDataOptionStructure':  # noqa: C901
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
        if 'options' in data:
            self.options = list()
            for option_dict in data['options']:
                self.options.append(InteractionDataOptionStructure().from_dict(option_dict))
        return self


class InteractionResponse(BaseDiscordObject):

    INTERACTION_RESPONSE_TYPES = enumerations.INTERACTION_RESPONSE_TYPES

    type: enumerations.INTERACTION_RESPONSE_TYPES
    data: 'InteractionCallback'

    # The following are part of our local book keeping, not the discord structure.
    interaction_id: 'snowflake.Snowflake'
    interaction_token: str

    def __init__(self):
        self.data = InteractionCallback()

    def to_dict(self) -> dict:
        new_dict: Dict[str, object] = dict()
        new_dict['type'] = self.type.value
        new_dict['data'] = self.data.to_dict()
        return new_dict

    async def send(self):
        await api.API.interaction_respond(self.interaction_id, self.interaction_token, self.to_dict())


class InteractionCallback(BaseDiscordObject, ext_components.ComponentAdder):
    tts: Optional[bool]
    content: Optional[str]
    # embeds: List[embeds]  # TODO: Support embeds here.
    # allowed_mentions: dict
    flags: int
    components: Optional[List[ext_components.Component]]

    def __init__(self):
        self.flags = 0

    def to_dict(self) -> dict:
        new_dict: Dict[str, object] = dict()
        new_dict['flags'] = self.flags
        if hasattr(self, 'tts'):
            new_dict['tts'] = self.tts
        if hasattr(self, 'content'):
            new_dict['content'] = self.content
        if hasattr(self, 'components'):
            new_dict['components'] = list()
            assert type(new_dict['components']) is list
            assert type(self.components) is list
            for component in self.components:
                new_dict['components'].append(component.to_dict())
        return new_dict

    def generate(self,
                 tts: Optional[bool] = None,
                 content: Optional[str] = None,
                 flags: int = 0,
                 ):
        if tts is not None:
            self.tts = tts
        if content is not None:
            self.content = content
        self.flags = flags
        if hasattr(self, 'components'):
            del self.components
