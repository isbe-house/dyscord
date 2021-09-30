
from src.simple_discord.objects.snowflake import Snowflake
from src.simple_discord.objects.interactions import InteractionStructure
from . import samples


def test_button_press():
    data = samples.button_press_interaction
    obj = InteractionStructure().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])


def test_text_command():
    data = samples.trigger_chat
    obj = InteractionStructure().from_dict(data)
    assert obj.application_id == Snowflake(data['application_id'])
