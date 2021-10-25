'''Commands that can be registered with the API.'''

import abc
import builtins
import copy
import re
from typing import Optional, Union, List, Dict

from ...client import api

from ..base_object import BaseDiscordObject

from .. import snowflake, guild as ext_guild

from . import enumerations


class Command(BaseDiscordObject):
    '''Command root used to generate new commands.

    Attributes:
        COMMAND_TYPE (COMMAND_TYPE): Helper pointer to the COMMAND_TYPE enumeration.
        COMMAND_OPTION (COMMAND_OPTION): Helper pointer to the COMMAND_OPTION enumeration.
        id (Snowflake): Unique ID of the command.
        type (Optional[COMMAND_TYPE]): Type of the command.
        application_id: (Snowflake): Unique id of the parent application.

    '''

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
        '''Return string representation.'''
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
        '''Helper function to generate a new command bound for registration.'''
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
        '''Add SubCommand to the command.'''
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
        '''Add SubCommandGroup to the command.'''
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
        '''Add option to the command.'''
        new_option = CommandOptions()  # type: ignore
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
        '''Remove all options.'''
        if hasattr(self, 'options'):
            del self.options

    async def register_to_guild(self, guild: 'Union[ext_guild.Guild, snowflake.Snowflake]') -> dict:
        '''Register a Command to a specific guild discord scope.

        Note that discord will limit you to 200 of these calls per bot per guild per day.
        '''
        if isinstance(guild, snowflake.Snowflake):
            guild_id = guild
        elif isinstance(guild, ext_guild.Guild):
            guild_id = guild.id
        return await api.API.create_guild_application_command(guild_id, self.to_dict())

    async def register_globally(self) -> dict:
        '''Register a Command to the global discord scope.

        Note that discord will limit you to 200 of these calls per bot per day.
        '''
        return await api.API.create_global_application_command(self.to_dict())

    def from_dict(self, data: dict) -> 'Command':
        '''Parse a Command from an API compliant dict.'''
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
        '''Convert object to dictionary suitable for API or other generic useage.'''
        ret_dict: Dict[str, Union[object, list]] = dict()
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
        '''Validate object is prepared for dispatch to discord.'''
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

        assert self.total_characters() <= 4000,\
            f'Found {self.total_characters():d} characters in name, description, and value fields. Max is 4,000.'

    def total_characters(self) -> int:
        '''Get the total characters in the name, description, and value.'''
        total_characters = 0
        if hasattr(self, 'name') and type(self.name) is str:
            total_characters += len(self.name)
        if hasattr(self, 'description') and type(self.description) is str:
            total_characters += len(self.description)
        if hasattr(self, 'options') and type(self.options) is list:
            for option in self.options:
                total_characters += option.total_characters()
        return total_characters


class CommandOptionsBase(BaseDiscordObject, abc.ABC):
    '''Abstract base for options.'''

    # Handy shortcut
    COMMAND_OPTION = enumerations.COMMAND_OPTION

    type: 'enumerations.COMMAND_OPTION'                       # one of application command option type the type of option
    name: str                                                 # string 1-32 character name
    description: str                                          # string 1-100 character description
    required: bool                                            # boolean if the parameter is required or optional--default false
    choices: Optional[List['CommandOptionChoiceStructure']]   # array of application command option choice choices for STRING, INTEGER, and
    # NUMBER types for the user to pick from, max 25
    options: Optional[List['CommandOptions']]                 # array of application command option if the option is a subcommand or subcommand group type,
    # this nested options will be the parameters

    def from_dict(self, data: dict) -> 'CommandOptionsBase':
        '''Parse a CommandOptionsBase from an API compliant dict.'''
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
        '''Convert object to dictionary suitable for API or other generic useage.'''
        ret_dict: Dict[str, Union[object, list]] = dict()
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
        '''Validate object is prepared for dispatch to discord.'''
        regex = r'^[\w-]{1,32}$'
        if not re.match(regex, self.name):
            raise ValueError(f'Name of \'{self.name}\' does not match \'{regex}\'.')

        if self.name != self.name.lower():
            raise ValueError('Command name must use lower case version of all characters.')

        if hasattr(self, 'choices') and self.choices is not None:
            for choice in self.choices:
                choice.validate()

        if hasattr(self, 'options') and self.options is not None:
            for option in self.options:
                option.validate()

    def total_characters(self) -> int:
        '''Get the total characters in the name, description, and value.'''
        total_characters = 0
        if hasattr(self, 'name') and type(self.name) is str:
            total_characters += len(self.name)
        if hasattr(self, 'description') and type(self.description) is str:
            total_characters += len(self.description)

        if hasattr(self, 'choices') and type(self.choices) is list:
            for choice in self.choices:
                total_characters += choice.total_characters()
        if hasattr(self, 'options') and type(self.options) is list:
            for option in self.options:
                total_characters += option.total_characters()
        return total_characters


class CommandOptions(CommandOptionsBase):
    '''Options for a Command.'''

    def add_choice(self,
                   name: str,
                   value: Union[str, int, float],
                   ) -> 'CommandOptionChoiceStructure':
        '''Append a choice to the given set of options and return it. Will start a list if needed.'''
        new_choice = CommandOptionChoiceStructure()
        new_choice.name = name
        new_choice.value = value
        if not hasattr(self, 'choices') or self.choices is None:
            self.choices = list()
        self.choices.append(new_choice)

        return new_choice

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
        return super().validate()


class CommandOptionSubCommandGroup(CommandOptionsBase):
    '''Intermediate object to group SubCommands together.'''
    # Same thing, let's just take it!
    add_option_sub_command = Command.add_option_sub_command


class CommandOptionSubCommand(CommandOptionsBase):
    '''Commands which live under a Command, or a Sub Command Group.'''

    COMMAND_OPTION = enumerations.COMMAND_OPTION

    add_option_typed = Command.add_option_typed


class CommandOptionChoiceStructure(BaseDiscordObject):
    '''Specific option for a command.'''

    def __init__(self):
        '''Initalize a CommandOptionChoiceStructure.'''
        self.name: str
        self.value: Union[str, int, float]

    def from_dict(self, data: dict) -> 'CommandOptionChoiceStructure':
        '''Parse a CommandOptionChoiceStructure from an API compliant dict.'''
        self.name = data['name']
        self.value = data['value']
        if type(self.value) not in [str, int, float]:
            raise ValueError(f'Value must be in [str, int, float], got {type(self.value)}')

        return self

    def to_dict(self) -> dict:
        '''Convert object to dictionary suitable for API or other generic useage.'''
        ret_dict: Dict[str, object] = dict()
        ret_dict['name'] = self.name
        ret_dict['value'] = self.value

        return ret_dict

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
        regex = r'^[\w-]{1,32}$'
        if not re.match(regex, self.name):
            raise ValueError(f'Name of \'{self.name}\' does not match \'{regex}\'.')

        if len(self.name) < 1 or len(self.name) > 100:
            raise ValueError(f'Length of name is {len(self.name)}, but be [1-100].')

    def total_characters(self) -> int:
        '''Get the total characters in the name, description, and value.'''
        total_characters = 0
        if hasattr(self, 'name') and type(self.name) is str:
            total_characters += len(self.name)
        if hasattr(self, 'value') and type(self.value) is str:
            total_characters += len(self.value)
        return total_characters
