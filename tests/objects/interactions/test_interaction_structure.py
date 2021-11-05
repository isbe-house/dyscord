import pytest
from unittest.mock import AsyncMock

from src.dyscord.objects.snowflake import Snowflake
from src.dyscord.objects.interactions import Interaction, Command, enumerations
from . import samples
from ..channel import samples as channel_samples
from ..role import samples as role_samples

from ...fixtures import mock_api  # noqa: F401


def test_button_interaction():
    data = samples.button_press_interaction
    obj = Interaction().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')


def test_text_interaction(mock_api):  # noqa: F811
    mock_api.get_user = AsyncMock(return_value=samples.trigger_chat['data']['resolved']['users']['185846097284038656'])

    data = samples.trigger_chat
    obj = Interaction().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')
    mock_api.get_user.assert_not_called()

    assert obj.can_respond
    assert not obj.can_followup

    response = obj.generate_response(ephemeral=True)
    ar = response.add_components()
    ar.add_button(ar.BUTTON_STYLES.PRIMARY, 'foo', 'My Button')
    ar.add_select_menu('bar', 'placeholder?')

    assert response.data.flags & enumerations.INTERACTION_CALLBACK_FLAGS.EPHEMERAL

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


def test_complex_chat(mock_api):  # noqa: F811

    data = samples.nested_groups
    obj = Interaction().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
    assert hasattr(obj, 'data')

    assert obj.data is not None

    assert type(obj.data.options) is dict
    assert obj.data.options['edit']['user']['target'].value.username == 'Soton'
    mock_api.get_user.assert_not_called()


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


def test_all_types(mock_api):  # noqa: F811
    mock_api.get_channel = AsyncMock(return_value=channel_samples.dev_guild_text)
    mock_api.get_user = AsyncMock(side_effect=RuntimeError)
    mock_api.get_guild_roles = AsyncMock(return_value=[role_samples.dev_role])

    obj = Interaction().from_dict(samples.all_types)
    assert obj is not None
    mock_api.get_channel.assert_not_called()
    print(mock_api.get_user.call_args)
    mock_api.get_user.assert_not_called()
    mock_api.get_guild_roles.assert_not_called()


def test_simple_interaction():

    for sample in samples.raw_interaction_create_samples:
        obj = Interaction()
        obj.from_dict(sample['d'])


@pytest.mark.asyncio
async def test_responses(mock_api):  # noqa: F811

    obj = Interaction()
    obj.from_dict(samples.raw_interaction_create_samples[0]['d'])

    with pytest.raises(RuntimeError):
        obj.generate_followup()

    response = obj.generate_response()

    with pytest.raises(RuntimeError):
        obj.generate_response()

    await response.send()
    mock_api.create_interaction_response.assert_called()

    followup = obj.generate_followup()

    followup.generate('This is a follow up')
    await followup.send()
    await followup.edit_original_response()
    await followup.edit_followup_message()
    await followup.delete_followup_message()
    await followup.delete_initial_response()
    mock_api.create_followup_message.assert_called()
    mock_api.edit_original_interaction_response.assert_called()
    mock_api.delete_original_interaction_response.assert_called()
    mock_api.edit_followup_message.assert_called()
    mock_api.delete_followup_message.assert_called()


def test_invalid_interaction_data():

    data = samples.all_types

    data['data']['resolved']['foo'] = {'Bad': 'Type'}

    with pytest.raises(TypeError):
        Interaction().from_dict(data)


def test_simple_unresolved_fields():

    data = samples.interaction_simple_data

    Interaction().from_dict(data)
