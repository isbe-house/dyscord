from src.dyscord.objects.snowflake import Snowflake
from src.dyscord.objects.interactions import Interaction, Command, enumerations
from . import samples
from ..channel import samples as channel_samples
from ..user import samples as user_samples
from ..role import samples as role_samples

from unittest.mock import AsyncMock, patch


def test_button_interaction():
    data = samples.button_press_interaction
    obj = Interaction().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')


@patch('src.dyscord.client.api.API')
def test_text_interaction(api_mock):
    api_mock.get_user = AsyncMock(return_value=samples.trigger_chat['data']['resolved']['users']['185846097284038656'])

    data = samples.trigger_chat
    obj = Interaction().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')
    api_mock.get_user.assert_called()

    assert obj.can_respond
    assert not obj.can_followup

    response = obj.generate_response()
    ar = response.add_components()
    ar.add_button(ar.BUTTON_STYLES.PRIMARY, 'foo', 'My Button')
    ar.add_select_menu('bar', 'placeholder?')

    followup = obj.generate_followup()
    followup.generate('This is a followup message!', tts=True)

    assert followup
    assert not obj.can_respond
    assert obj.can_followup


def test_message():
    data = samples.message_trigger_interaction
    obj = Interaction().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')


@patch('src.dyscord.client.api.api_v9.API_V9.get_user')
def test_complex_chat(get_user_func):

    get_user_func.return_value = {'avatar': 'b437e9bd4b0e487a097c4538c6cdce3f',
                                  'discriminator': '2585',
                                  'id': '185846097284038656',
                                  'public_flags': 0,
                                  'username': 'Soton'}

    data = samples.nested_groups
    obj = Interaction().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')

    assert obj.data is not None

    assert type(obj.data.options) is dict
    print(obj.data.options['edit'].options['user'].options['target'])
    assert obj.data.options['edit'].options['user'].options['target'].username == 'Soton'


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


@patch('src.dyscord.client.api.API')
def test_all_types(api_mock):
    api_mock.get_channel = AsyncMock(return_value=channel_samples.dev_guild_text)
    api_mock.get_user = AsyncMock(return_value=user_samples.raw_get_user_response)
    api_mock.get_guild_roles = AsyncMock(return_value=[role_samples.dev_role])

    obj = Interaction().from_dict(samples.all_types)
    assert obj is not None
    api_mock.get_channel.assert_called()
    api_mock.get_user.assert_called()
    api_mock.get_guild_roles.assert_called()
