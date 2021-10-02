
from src.simple_discord.objects.snowflake import Snowflake
from src.simple_discord.objects.interactions import InteractionStructure
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
