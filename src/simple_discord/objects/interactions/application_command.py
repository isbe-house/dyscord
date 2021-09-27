import copy
import re
from typing import Optional, Union, List
import builtins


from ..base_object import BaseDiscordObject
from .. import snowflake
from ... import objects
from . import enumerations


class Interactions:

    async def generate_command(self):
        pass


class Command(BaseDiscordObject):

    COMMAND_TYPE = enumerations.COMMAND_TYPE

    def __init__(self):
        self.id: Optional[snowflake.Snowflake]              # unique id of the command  all
        self.type: Optional[enumerations.COMMAND_TYPE]  # one of application command type  the type of command, defaults 1 if not set  all
        self.application_id: Optional[snowflake.Snowflake]  # unique id of the parent application  all
        self.guild_id: Optional[snowflake.Snowflake]        # guild id of the command, if not global  all
        self.name: str                                      # 1-32 character name  all
        self.description: str                               # 1-100 character description for CHAT_INPUT commands, empty string for USER and MESSAGE commands  all
        self.options: Optional[list[CommandOptions]]        # array of application command option  the parameters for the command, max 25  CHAT_INPUT
        self.default_permission: bool                       # boolean (default true)  whether the command is enabled by default when the app is added to a guild  all
        self.version: Optional[snowflake.Snowflake]         # autoincrementing version identifier updated during substantial record changes  all

    def generate(self,
                 name: str,
                 description: str,
                 type: 'enumerations.COMMAND_TYPE',
                 options: Optional[List['CommandOptions']] = None,
                 default_permission: bool = True,
                 ):
        '''
        Helper function to generate a new command bound for registration.
        '''
        self.name = name
        self.description = description
        self.default_permission = default_permission
        self.type = type

        if options is not None:
            self.options = copy.deepcopy(options)
        elif options is None and hasattr(self, 'options'):
            del self.options

    def add_option_sub_command(self):
        raise NotImplementedError

    def add_option_sub_command_group(self):
        raise NotImplementedError

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

    async def register_to_guild(self, guild: objects.guild.Guild):
        pass

    async def register_globally(self, guild: objects.guild.Guild):
        pass

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
                if type(option) is not CommandOptions:
                    raise TypeError(f'Found option of type {type(option)}, must be {CommandOptions}')
                option.validate()

        if type(self.default_permission) is not bool:
            raise TypeError(f'Default Permission is of incorrect type {type(self.default_permission)}, should be {type(True)}.')


class CommandOptions(BaseDiscordObject):

    # Handy shortcut
    COMMAND_OPTION = enumerations.COMMAND_OPTION

    def __init__(self):
        self.type: enumerations.COMMAND_OPTION                      # one of application command option type the type of option
        self.name: str                                                          # string 1-32 character name
        self.description: str                                                   # string 1-100 character description
        self.required: bool                                                     # boolean if the parameter is required or optional--default false
        self.choices: Optional[list[CommandOptionChoiceStructure]]   # array of application command option choice choices for STRING, INTEGER, and
        # NUMBER types for the user to pick from, max 25
        self.options: Optional[list[CommandOptions]]                 # array of application command option if the option is a subcommand or subcommand group type,
        # this nested options will be the parameters

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

    def from_dict(self, data: dict) -> 'CommandOptions':
        if 'type' in data:
            self.type = enumerations.COMMAND_OPTION(data['type'])
        self.name = data['name']
        self.description = data['description']
        if 'required' in data:
            self.required = data['required']
        if 'choices' in data:
            # TODO: Loop through and process the options.
            # self.choices
            pass
        if 'options' in data:
            # TODO: Loop through and process the options.
            # self.options
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


class CommandInteractionDataOptionStructure(BaseDiscordObject):

    def __init__(self):
        self.name: str                                                          # string the name of the parameter
        self.type: enumerations.COMMAND_OPTION                      # integer value of application command option type
        self.value: enumerations.COMMAND_OPTION                     # application command option type the value of the pair
        self.options: list[CommandInteractionDataOptionStructure]    # ? array of application command interaction data option present if this option is a group or subcommand

    def from_dict(self, data: dict) -> 'CommandInteractionDataOptionStructure':
        self.name = data['name']
        self.type = enumerations.COMMAND_OPTION(data['type'])
        if 'value' in data:
            self.value = enumerations.COMMAND_OPTION[data['value']]
        if 'options' in data:
            self.options = list()
            for option in data['options']:
                new_option = CommandInteractionDataOptionStructure()
                new_option.from_dict(option)
                self.options.append(new_option)

        return self

    def to_dict(self) -> dict:
        ret_dict: dict[str, Union[object, list]] = dict()
        ret_dict['name'] = self.name
        ret_dict['type'] = self.type.value
        if hasattr(self, 'value'):
            ret_dict['value'] = self.value.value
        if hasattr(self, 'options'):
            ret_dict['options'] = list()
            assert type(ret_dict['options']) is list
            for option in self.options:
                ret_dict['options'].append(option.to_dict())

        return ret_dict

    def validate(self):
        regex = r'^[\w-]{1,32}$'
        if not re.match(regex, self.name):
            raise ValueError(f'Name of \'{self.name}\' does not match \'{regex}\'.')
