import copy
import enum
import re
from typing import Optional, Union, List

from ..base_object import BaseDiscordObject
from .. import snowflake
from ... import objects


class Interactions:

    async def generate_command(self):
        pass


class CommandStructure(BaseDiscordObject):

    class COMMAND_TYPE(enum.IntEnum):
        CHAT_INPUT = 1  # Slash commands; a text-based command that shows up when a user types /
        USER = 2  # A UI-based command that shows up when you right click or tap on a user
        MESSAGE = 3  # A UI-based command that shows up when you right click or tap on a message

    def __init__(self):
        self.id: Optional[snowflake.Snowflake]              # unique id of the command  all
        self.type: Optional[CommandStructure.COMMAND_TYPE]  # one of application command type  the type of command, defaults 1 if not set  all
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
                 type: 'CommandStructure.COMMAND_TYPE',
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
                         type: 'CommandOptions.COMMAND_OPTION',
                         name: str,
                         description: str,
                         required: bool = True,
                         choices: Optional[List['CommandOptionChoiceStructure']] = None,
                         ) -> 'CommandOptions':
        if not hasattr(self, 'options') or self.options == None:
            self.options = list()
        new_option = CommandOptions()
        new_option.type = type
        new_option.name = name
        new_option.description = description
        new_option.required = required
        if choices is not None:
            new_option.choices = copy.deepcopy(choices)
        self.options.append(new_option)

        return new_option

    def clear_options(self):
        if hasattr(self, 'options'):
            del self.options

    async def register_to_guild(self, guild: objects.guild.Guild):
        pass

    async def register_globally(self, guild: objects.guild.Guild):
        pass

    def from_dict(self, data: dict) -> 'CommandStructure':
        if 'id' in data:
            self.id = snowflake.Snowflake(data['id'])
        if 'type' in data:
            self.type = self.COMMAND_TYPE(data['type'])
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

    def validate(self):
        regex = r'^[\w-]{1,32}$'
        if not re.match(regex, self.name):
            raise ValueError(f'Name of \'{self.name}\' does not match \'{regex}\'.')

        if self.name != self.name.lower():
            raise ValueError(f'Command name must use lower case version of all characters.')

        if self.type in [self.COMMAND_TYPE.USER, self.COMMAND_TYPE.MESSAGE]:
            if len(self.description):
                raise ValueError(f'Descriptions are not allowed for type {self.type.name} commands.')
        elif self.type == self.COMMAND_TYPE.CHAT_INPUT:
            if not len(self.description):
                raise ValueError(f'Descriptions are mandatory {self.type.name} commands.')

        if type(self.options) is list:
            if len(self.options) and self.type in [self.COMMAND_TYPE.USER, self.COMMAND_TYPE.MESSAGE]:
                raise ValueError(f'Context menu commands cannot have options.')

            for option in self.options:
                option.validate()


class CommandOptions(BaseDiscordObject):

    class COMMAND_OPTION(enum.IntEnum):
        SUB_COMMAND = 1
        SUB_COMMAND_GROUP = 2
        STRING = 3
        INTEGER = 4  # Any integer between -2^53 and 2^53
        BOOLEAN = 5
        USER = 6
        CHANNEL = 7  # Includes all channel types + categories
        ROLE = 8
        MENTIONABLE = 9  # Includes users and roles
        NUMBER = 10  # Any double between -2^53 and 2^53

    def __init__(self):
        self.type: CommandOptions.COMMAND_OPTION                      # one of application command option type the type of option
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
            self.type = self.COMMAND_OPTION(data['type'])
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
            raise ValueError(f'Command name must use lower case version of all characters.')

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
        self.type: CommandOptions.COMMAND_OPTION                      # integer value of application command option type
        self.value: CommandOptions.COMMAND_OPTION                     # application command option type the value of the pair
        self.options: list[CommandInteractionDataOptionStructure]    # ? array of application command interaction data option present if this option is a group or subcommand

    def from_dict(self, data: dict) -> 'CommandInteractionDataOptionStructure':
        self.name = data['name']
        self.type = CommandOptions.COMMAND_OPTION(data['type'])
        if 'value' in data:
            self.value = CommandOptions.COMMAND_OPTION[data['value']]
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
