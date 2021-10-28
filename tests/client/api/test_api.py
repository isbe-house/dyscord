from importlib import reload
from unittest.mock import sentinel, Mock

import pytest

from src.dyscord.client.api import api_v9
from src.dyscord.objects import Snowflake

from ...fixtures import mock_httpx  # noqa: F401


@pytest.fixture
def fresh_api():
    reload(api_v9)
    api_v9.API_V9.TOKEN = sentinel.TOKEN
    api_v9.API_V9.APPLICATION_ID = sentinel.APPLICATION_ID
    yield api_v9.API_V9


@pytest.mark.asyncio
async def test_get_gateway_bot(mock_httpx, fresh_api):  # noqa: F811
    fresh_api._auth_header()
    mock_httpx.return_value.get.return_value.json = Mock(return_value={'url': 'https://example.com/gateway'})

    fake_token = Mock(str)

    ret = await fresh_api.get_gateway_bot(fake_token)

    assert isinstance(ret, dict)

    assert ret['url'] == 'https://example.com/gateway?v=9&encoding=json'


@pytest.mark.asyncio
async def test_get_gateway(mock_httpx, fresh_api):  # noqa: F811

    ret = await fresh_api.get_gateway()
    assert ret == sentinel.JSON_RETURN


@pytest.mark.asyncio
async def test_get_global_application_commands(mock_httpx, fresh_api):  # noqa: F811

    ret = await fresh_api.get_global_application_commands()
    assert ret == sentinel.JSON_RETURN


@pytest.mark.asyncio
async def test_create_global_application_command(mock_httpx, fresh_api):  # noqa: F811

    fake_dict = Mock(dict)

    ret = await fresh_api.create_global_application_command(fake_dict)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.create_global_application_command(None)


@pytest.mark.asyncio
async def test_get_global_application_command(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)

    ret = await fresh_api.get_global_application_command(fake_id)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.get_global_application_command(None)


@pytest.mark.asyncio
async def test_edit_global_application_command(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)
    fake_dict = Mock(dict)

    ret = await fresh_api.edit_global_application_command(fake_id, fake_dict)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.edit_global_application_command(None, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.edit_global_application_command(fake_id, None)


@pytest.mark.skip(reason='Not implemeted yet.')
@pytest.mark.asyncio
async def test_bulk_overwrite_global_application_commands(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)

    ret = await fresh_api.bulk_overwrite_global_application_commands(fake_id)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.bulk_overwrite_global_application_commands(None)


@pytest.mark.asyncio
async def test_get_guild_application_commands(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)

    ret = await fresh_api.get_guild_application_commands(fake_id)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.get_guild_application_commands(None)


@pytest.mark.asyncio
async def test_create_guild_application_command(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)
    fake_dict = Mock(dict)

    ret = await fresh_api.create_guild_application_command(fake_id, fake_dict)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.create_guild_application_command(None, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.create_guild_application_command(fake_id, None)


@pytest.mark.asyncio
async def test_get_guild_application_command(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)

    ret = await fresh_api.get_guild_application_command(fake_id, fake_id)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.get_guild_application_command(None, fake_id)

    with pytest.raises(TypeError):
        await fresh_api.get_guild_application_command(fake_id, None)


@pytest.mark.skip(reason='Not implemented yet')
@pytest.mark.asyncio
async def test_edit_guild_application_command(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)
    fake_dict = Mock(dict)

    ret = await fresh_api.edit_guild_application_command(fake_id, fake_id, fake_dict)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.edit_guild_application_command(None, fake_id, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.edit_guild_application_command(fake_id, None, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.edit_guild_application_command(fake_id, fake_id, None)


@pytest.mark.asyncio
async def test_delete_guild_application_command(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)

    await fresh_api.delete_guild_application_command(fake_id, fake_id)

    with pytest.raises(TypeError):
        await fresh_api.delete_guild_application_command(None, fake_id)

    with pytest.raises(TypeError):
        await fresh_api.delete_guild_application_command(fake_id, None)


@pytest.mark.skip(reason='Not implemented yet')
@pytest.mark.asyncio
async def test_bulk_overwrite_guild_application_command(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)
    fake_dict = Mock(dict)

    ret = await fresh_api.bulk_overwrite_guild_application_command(fake_id, fake_id, fake_dict)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.bulk_overwrite_guild_application_command(None, fake_id, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.bulk_overwrite_guild_application_command(fake_id, None, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.bulk_overwrite_guild_application_command(fake_id, fake_id, None)


@pytest.mark.asyncio
async def test_create_interaction_response(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)
    fake_token = Mock(str)
    fake_dict = Mock(dict)

    await fresh_api.create_interaction_response(fake_id, fake_token, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.create_interaction_response(None, fake_token, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.create_interaction_response(fake_id, None, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.create_interaction_response(fake_id, fake_token, None)


@pytest.mark.asyncio
async def test_edit_original_interaction_response(mock_httpx, fresh_api):  # noqa: F811

    fake_token = Mock(str)
    fake_dict = Mock(dict)

    await fresh_api.edit_original_interaction_response(fake_token, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.edit_original_interaction_response(None, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.edit_original_interaction_response(fake_token, None)


@pytest.mark.asyncio
async def test_delete_original_interaction_response(mock_httpx, fresh_api):  # noqa: F811

    fake_token = Mock(str)

    await fresh_api.delete_original_interaction_response(fake_token)

    with pytest.raises(TypeError):
        await fresh_api.delete_original_interaction_response(None)


@pytest.mark.asyncio
async def test_create_followup_message(mock_httpx, fresh_api):  # noqa: F811

    fake_token = Mock(str)
    fake_dict = Mock(dict)

    ret = await fresh_api.create_followup_message(fake_token, fake_dict)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.create_followup_message(None, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.create_followup_message(fake_token, None)


@pytest.mark.asyncio
async def test_get_followup_message(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)
    fake_token = Mock(str)

    ret = await fresh_api.get_followup_message(fake_token, fake_id)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.get_followup_message(None, fake_id)

    with pytest.raises(TypeError):
        await fresh_api.get_followup_message(fake_token, None)


@pytest.mark.asyncio
async def test_edit_followup_message(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)
    fake_token = Mock(str)
    fake_dict = Mock(dict)

    ret = await fresh_api.edit_followup_message(fake_token, fake_id, fake_dict)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.edit_followup_message(None, fake_id, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.edit_followup_message(fake_token, None, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.edit_followup_message(fake_token, fake_id, None)


@pytest.mark.asyncio
async def test_delete_followup_message(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)
    fake_token = Mock(str)

    await fresh_api.delete_followup_message(fake_token, fake_id)
    mock_httpx.return_value.delete.assert_called()

    with pytest.raises(TypeError):
        await fresh_api.delete_followup_message(None, fake_id)

    with pytest.raises(TypeError):
        await fresh_api.delete_followup_message(fake_token, None)


@pytest.mark.asyncio
async def test_get_channel(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)

    ret = await fresh_api.get_channel(fake_id)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.get_channel(None)


@pytest.mark.asyncio
async def test_create_message(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)
    fake_dict = Mock(dict)

    ret = await fresh_api.create_message(fake_id, fake_dict)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.create_message(None, fake_dict)

    with pytest.raises(TypeError):
        await fresh_api.create_message(fake_id, None)


@pytest.mark.asyncio
async def test_get_guild(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)

    ret = await fresh_api.get_guild(fake_id)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.get_guild(None)


@pytest.mark.asyncio
async def test_get_guild_roles(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)

    ret = await fresh_api.get_guild_roles(fake_id)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.get_guild_roles(None)


@pytest.mark.asyncio
async def test_get_current_user(mock_httpx, fresh_api):  # noqa: F811

    ret = await fresh_api.get_current_user()
    assert ret == sentinel.JSON_RETURN


@pytest.mark.asyncio
async def test_get_user(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)

    ret = await fresh_api.get_user(fake_id)
    assert ret == sentinel.JSON_RETURN

    with pytest.raises(TypeError):
        await fresh_api.get_user(None)


@pytest.mark.asyncio
async def test_create_dm(mock_httpx, fresh_api):  # noqa: F811

    fake_id = Mock(Snowflake)

    ret = await fresh_api.create_dm(fake_id)
    assert ret == sentinel.JSON_RETURN

    mock_httpx.return_value.post.assert_called()

    with pytest.raises(TypeError):
        await fresh_api.create_dm(None)
