
import orjson as json

from src.simple_discord.objects.interactions import CommandStructure, CommandOptions, CommandOptionChoiceStructure, CommandInteractionDataOptionStructure
from src.simple_discord.objects import Snowflake


def test_ACS():

    x = CommandStructure()

    input_dict = {
        'id': '12345',
        'type': 2,
        'application_id': str(Snowflake()),
        'guild_id': str(Snowflake()),
        'name': 'Test Command',
        'description': 'This is a test description',
        'default_permission': True,
        'version': str(Snowflake()),
    }

    x.from_dict(json.loads(json.dumps(input_dict)))

    assert x.id == Snowflake(input_dict['id'])
    assert x.type == CommandStructure.COMMAND_TYPE(input_dict['type'])
    assert x.application_id == Snowflake(input_dict['application_id'])
    assert x.guild_id == Snowflake(input_dict['guild_id'])
    assert x.name == input_dict['name']
    assert x.description == input_dict['description']
    assert x.default_permission == input_dict['default_permission']
    assert x.version == input_dict['version']


def test_ACO():

    x = CommandOptions()
    input_dict = {
        'type': CommandOptions.COMMAND_OPTION(3),
        'name': 'Test Command Option',
        'description': 'This is an example of an option',
        'required': True,
    }

    x.from_dict(input_dict)


def test_ACOCS():

    x = CommandOptionChoiceStructure()
    input_dict = {
        'name': 'Animal',
        'value': 'Frog',
    }
    x.from_dict(input_dict)


def test_ACIDOS():

    x = CommandInteractionDataOptionStructure()
    input_dict = {
        'name': 'Animal',
        'type': 2,
        'value': 'STRING',
    }
    x.from_dict(input_dict)


def test_build_command():
    # Create options
    o = CommandOptions()
    o.type = CommandOptions.COMMAND_OPTION.INTEGER
    o.name = 'Test Int'
    o.description = 'Just an int'

    x = CommandStructure()
    x.type = CommandStructure.COMMAND_TYPE.USER
    x.name = 'TEST'
    x.description = 'This is a test command.'
    x.options = list()
    x.options.append(o)
    data = x.to_dict()
    assert not hasattr(x, 'id')
    assert not hasattr(x, 'application_id')
    assert 'id' not in data

def test_generation():
    new_cmd = CommandStructure()
    new_cmd.generate(
        name='Test Command',
        description='This is a test of the command structure.',
    )
    new_cmd.to_dict()

    assert not hasattr(new_cmd, 'id')
