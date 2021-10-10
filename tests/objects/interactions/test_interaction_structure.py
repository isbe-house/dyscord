from src.simple_discord.objects.snowflake import Snowflake
from src.simple_discord.objects.interactions import InteractionStructure, Command, enumerations
from . import samples


def test_button_interaction():
    data = samples.button_press_interaction
    obj = InteractionStructure().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')


def test_text_interaction():
    data = samples.trigger_chat
    obj = InteractionStructure().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')


def test_message():
    data = samples.message_trigger_interaction
    obj = InteractionStructure().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')


def test_complex_chat():
    data = samples.nested_groups
    obj = InteractionStructure().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')

    assert obj.data is not None

    assert obj.data.options[0].options[0].options[0].name == 'target'


def test_build_sub_commands():

    new_command = Command()
    new_command.generate(name='test-command', description='This is a test description', type=enumerations.COMMAND_TYPE.CHAT_INPUT)

    new_command.validate()

    sc = new_command.add_option_sub_command('sub-test', description='Test of the sub description.')

    sc.add_option_typed(sc.COMMAND_OPTION.USER, 'target', 'Target to hit', required=False)

    new_command.validate()


def test_build_sub_commands_groups():

    new_command = Command()
    new_command.generate(name='test-command', description='This is a test description', type=enumerations.COMMAND_TYPE.CHAT_INPUT)

    new_command.validate()

    scg = new_command.add_option_sub_command_group('group', description='A sub command group')

    sc = scg.add_option_sub_command('sub-test', description='Test of the sub description.')

    sc.add_option_typed(sc.COMMAND_OPTION.USER, 'target', 'Target to hit', required=False)

    new_command.validate()
