import abc
import builtins
import copy
import re
from collections import defaultdict
from typing import Optional, Union, List, Dict


from ...client import api

from ..base_object import BaseDiscordObject

from .. import snowflake,\
    guild

from .. import user as ext_user,\
    message as ext_message

from . import enumerations,\
    components as ext_components


class Interactions(BaseDiscordObject):

    async def generate_command(self):
        pass


class ComponentAdder(abc.ABC):

    '''Allow other objects to start adding components to themselves with a common set of helper functions.

    Caution: This is an abstract class, and is not intended for direct instantiation.
    '''

    def add_components(self) -> 'ext_components.ActionRow':
        '''
        Start adding components by starting an ACTION_ROW.
        '''
        if not hasattr(self, 'components'):
            self.components: Optional[List['ext_components.Component']] = list()
        assert type(self.components) is list
        new_action_row = ext_components.ActionRow()
        self.components.append(new_action_row)

        return new_action_row


class Command(BaseDiscordObject):

    COMMAND_TYPE = enumerations.COMMAND_TYPE
    COMMAND_OPTION = enumerations.COMMAND_OPTION

    id: 'snowflake.Snowflake'                        # unique id of the command  all
    type: Optional['enumerations.COMMAND_TYPE']      # one of application command type  the type of command, defaults 1 if not set  all
    application_id: Optional['snowflake.Snowflake']  # unique id of the parent application  all
    guild_id: Optional['snowflake.Snowflake']        # guild id of the command, if not global  all
    name: str                                        # 1-32 character name  all
    description: str                                 # 1-100 character description for CHAT_INPUT commands, empty string for USER and MESSAGE commands  all
    options: Optional[List['CommandOptionsBase']]    # array of application command option  the parameters for the command, max 25  CHAT_INPUT
    default_permission: bool                         # boolean (default true)  whether the command is enabled by default when the app is added to a guild  all
    version: Optional['snowflake.Snowflake']         # autoincrementing version identifier updated during substantial record changes  all

    def __str__(self):
        fields = list()

        if hasattr(self, 'id'):
            fields.append(f'id={self.id}')
        if hasattr(self, 'type') and type(self.type) is enumerations.COMPONENT_TYPES:
            fields.append(f'type={self.type.name}')
        if hasattr(self, 'name'):
            fields.append(f'name=\'{self.name}\'')
        if hasattr(self, 'description'):
            fields.append(f'description=\'{self.description}\'')
        if hasattr(self, 'version'):
            fields.append(f'version={self.version}')

        return f'Command({", ".join(fields)})'

    def generate(self,
                 name: str,
                 description: str,
                 type: 'enumerations.COMMAND_TYPE',
                 options: Optional[List['CommandOptionsBase']] = None,
                 default_permission: bool = True,
                 ):
        '''
        Helper function to generate a new command bound for registration.
        '''
        self.name = name
        self.description = description
        self.default_permission = default_permission
        self.type = type

        if builtins.type(options) is list:
            self.options = copy.deepcopy(options)
        elif options is None and hasattr(self, 'options'):
            del self.options

    def add_option_sub_command(self,
                               name: str,
                               description: str,
                               ) -> 'CommandOptionSubCommand':
        new_option = CommandOptionSubCommand()
        new_option.type = enumerations.COMMAND_OPTION.SUB_COMMAND
        new_option.name = name
        new_option.description = description

        if not hasattr(self, 'options'):
            self.options = list()

        assert type(self.options) is list
        self.options.append(new_option)

        return new_option

    def add_option_sub_command_group(self,
                                     name: str,
                                     description: str,
                                     ) -> 'CommandOptionSubCommandGroup':
        new_option = CommandOptionSubCommandGroup()
        new_option.type = enumerations.COMMAND_OPTION.SUB_COMMAND_GROUP
        new_option.name = name
        new_option.description = description

        if not hasattr(self, 'options'):
            self.options = list()

        assert type(self.options) is list
        self.options.append(new_option)

        return new_option

    def add_option_typed(self,
                         type: 'enumerations.COMMAND_OPTION',
                         name: str,
                         description: str,
                         required: bool = True,
                         choices: Optional[List['CommandOptionChoiceStructure']] = None,
                         ) -> 'CommandOptions':
        new_option = CommandOptions()
        new_option.type = type
        new_option.name = name
        new_option.description = description
        new_option.required = required
        if choices is not None:
            new_option.choices = copy.deepcopy(choices)

        if not hasattr(self, 'options') or self.options is None:
            self.options = list()
        assert builtins.type(self.options) is list
        self.options.append(new_option)

        return new_option

    def clear_options(self):
        if hasattr(self, 'options'):
            del self.options

    async def register_to_guild(self, guild: 'guild.Guild') -> dict:
        return await api.API.create_guild_application_command(guild.id, self.to_dict())

    async def register_globally(self) -> dict:
        return await api.API.create_global_application_command(self.to_dict())

    def from_dict(self, data: dict) -> 'Command':
        if 'id' in data:
            self.id = snowflake.Snowflake(data['id'])
        if 'type' in data:
            self.type = enumerations.COMMAND_TYPE(data['type'])
        if 'application_id' in data:
            self.application_id = data['application_id']
        if 'guild_id' in data:
            self.guild_id = data['guild_id']
        self.name = data['name']
        self.description = data['description']
        if 'options' in data:
            # TODO: Loop through and process the options.
            # self.options
            pass
        if 'default_permission' in data:
            self.default_permission = data['default_permission']
        if 'version' in data:
            self.version = data['version']

        return self

    def to_dict(self) -> dict:
        ret_dict: dict[str, Union[object, list]] = dict()
        if hasattr(self, 'id'):
            ret_dict['id'] = str(self.id)
        if hasattr(self, 'type') and self.type is not None:
            if type(self.type) is int:
                ret_dict['type'] = self.type
            else:
                ret_dict['type'] = self.type.value
        if hasattr(self, 'application_id'):
            ret_dict['application_id'] = str(self.application_id)
        if hasattr(self, 'guild_id'):
            ret_dict['guild_id'] = str(self.guild_id)
        ret_dict['name'] = self.name
        ret_dict['description'] = self.description
        if hasattr(self, 'options') and self.options is not None:
            ret_dict['options'] = list()
            assert type(ret_dict['options']) is list  # This has got to be the stupidest assert ever, but mypy wants it!
            for option in self.options:
                ret_dict['options'].append(option.to_dict())
        if hasattr(self, 'default_permission'):
            ret_dict['default_permission'] = self.default_permission
        if hasattr(self, 'version'):
            ret_dict['version'] = str(self.version)

        return ret_dict

    def validate(self):  # noqa: C901
        regex = r'^[\w-]{1,32}$'
        if not re.match(regex, self.name):
            raise ValueError(f'Name of \'{self.name}\' does not match \'{regex}\'.')

        if self.name != self.name.lower():
            raise ValueError('Command name must use lower case version of all characters.')

        if len(self.description) > 100:
            raise ValueError('Description cannot exceed 100 characters.')

        if self.type in [enumerations.COMMAND_TYPE.USER, enumerations.COMMAND_TYPE.MESSAGE]:
            if len(self.description):
                raise ValueError(f'Descriptions are not allowed for type {self.type.name} commands.')
        elif self.type == enumerations.COMMAND_TYPE.CHAT_INPUT:
            if not len(self.description):
                raise ValueError(f'Descriptions are mandatory {self.type.name} commands.')

        if type(self.type) is not enumerations.COMMAND_TYPE:
            raise TypeError(f'Type is of incorrect type {type(self.type)}, should be {enumerations.COMMAND_TYPE}.')

        if hasattr(self, 'options') and type(self.options) is list:

            if len(self.options) and self.type in [enumerations.COMMAND_TYPE.USER, enumerations.COMMAND_TYPE.MESSAGE]:
                raise ValueError('Context menu commands cannot have options.')

            if len(self.options) > 25:
                raise OverflowError(f'You cannot have {len(self.options)} options, limited to max of 25.')

            for option in self.options:
                if not isinstance(option, CommandOptionsBase):
                    raise TypeError(f'Found option of type {type(option)}, must be {CommandOptions}')
                option.validate()

        if type(self.default_permission) is not bool:
            raise TypeError(f'Default Permission is of incorrect type {type(self.default_permission)}, should be {type(True)}.')


class CommandOptionsBase(abc.ABC, BaseDiscordObject):

    # Handy shortcut
    COMMAND_OPTION = enumerations.COMMAND_OPTION

    type: 'enumerations.COMMAND_OPTION'                      # one of application command option type the type of option
    name: str                                                          # string 1-32 character name
    description: str                                                   # string 1-100 character description
    required: bool                                                     # boolean if the parameter is required or optional--default false
    choices: Optional[List['CommandOptionChoiceStructure']]   # array of application command option choice choices for STRING, INTEGER, and
    # NUMBER types for the user to pick from, max 25
    options: Optional[List['CommandOptions']]                 # array of application command option if the option is a subcommand or subcommand group type,
    # this nested options will be the parameters

    def from_dict(self, data: dict) -> 'CommandOptionsBase':
        if 'type' in data:
            self.type = enumerations.COMMAND_OPTION(data['type'])
        self.name = data['name']
        self.description = data['description']
        if 'required' in data:
            self.required = data['required']
        if 'choices' in data:
            # TODO: Loop through and process the choices.
            # self.choices
            pass
        if 'options' in data:
            # TODO: Loop through and process the options.
            # self.choices
            pass

        return self

    def to_dict(self) -> dict:
        ret_dict: dict[str, Union[object, list]] = dict()
        if hasattr(self, 'type'):
            ret_dict['type'] = self.type.value
        ret_dict['name'] = self.name
        ret_dict['description'] = self.description
        if hasattr(self, 'required'):
            ret_dict['required'] = self.required
        if hasattr(self, 'choices'):
            ret_dict['choices'] = list()
            assert type(ret_dict['choices']) is list  # This has got to be the stupidest assert ever, but mypy wants it!
            assert type(self.choices) is list
            for choice in self.choices:
                ret_dict['choices'].append(choice.to_dict())
        if hasattr(self, 'options'):
            ret_dict['options'] = list()
            assert type(ret_dict['options']) is list  # This has got to be the stupidest assert ever, but mypy wants it!
            assert type(self.options) is list
            for option in self.options:
                ret_dict['options'].append(option.to_dict())

        return ret_dict

    def validate(self):
        regex = r'^[\w-]{1,32}$'
        if not re.match(regex, self.name):
            raise ValueError(f'Name of \'{self.name}\' does not match \'{regex}\'.')

        if self.name != self.name.lower():
            raise ValueError('Command name must use lower case version of all characters.')

        if hasattr(self, 'choices') and self.choices is not None:
            for choice in self.choices:
                choice.validate()


class CommandOptions(CommandOptionsBase):

    def add_choice(self,
                   name: str,
                   value: Union[str, int, float],
                   ):
        new_choice = CommandOptionChoiceStructure()
        new_choice.name = name
        new_choice.value = value
        if not hasattr(self, 'choices') or self.choices is None:
            self.choices = list()
        self.choices.append(new_choice)

        return new_choice


class CommandOptionSubCommandGroup(CommandOptionsBase):
    # Same thing, let's just take it!
    add_option_sub_command = Command.add_option_sub_command


class CommandOptionSubCommand(CommandOptionsBase):

    COMMAND_OPTION = enumerations.COMMAND_OPTION

    add_option_typed = Command.add_option_typed


class CommandOptionChoiceStructure(BaseDiscordObject):

    def __init__(self):
        self.name: str
        self.value: Union[str, int, float]

    def from_dict(self, data: dict) -> 'CommandOptionChoiceStructure':
        self.name = data['name']
        self.value = data['value']
        if type(self.value) not in [str, int, float]:
            raise ValueError(f'Value must be in [str, int, float], got {type(self.value)}')

        return self

    def to_dict(self) -> dict:
        ret_dict: dict[str, object] = dict()
        ret_dict['name'] = self.name
        ret_dict['value'] = self.value

        return ret_dict

    def validate(self):
        regex = r'^[\w-]{1,32}$'
        if not re.match(regex, self.name):
            raise ValueError(f'Name of \'{self.name}\' does not match \'{regex}\'.')

        if len(self.name) < 1 or len(self.name) > 100:
            raise ValueError(f'Length of name is {len(self.name)}, but be [1-100].')


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

    def to_dict(self) -> dict:
        ret_dict: dict = dict()
        return ret_dict

    def validate(self):
        pass

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
    values: Optional[List[CommandOptions]]  # ? array of select option values the values the user selected Component (Select)
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


class InteractionCallback(BaseDiscordObject, ComponentAdder):
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
