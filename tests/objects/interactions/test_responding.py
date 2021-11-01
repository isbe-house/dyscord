
import pytest

from src.dyscord.objects.interactions import Interaction, InteractionResponse
from . import samples

from ...fixtures import mock_api  # noqa: F401


@pytest.mark.asyncio
async def test_respond_and_follow(mock_api):  # noqa: F811

    obj = Interaction().from_dict(samples.message_trigger_interaction)

    response = obj.generate_response()
    response.generate('Simple message')
    response_embeds = response.add_embeds()
    response_embeds.generate('Test Embed.')
    response.validate()

    followup = obj.generate_followup()
    followup.to_dict()

    with pytest.raises(ValueError, match=r'Must give specific followup message, or have sent one already.'):
        await followup.edit_followup_message()

    with pytest.raises(ValueError, match=r'Must give specific followup message, or have sent one already.'):
        await followup.delete_followup_message()

    followup_embeds = followup.add_embeds()
    followup_embeds.generate('Test Embed')

    followup_componenets = followup.add_components()
    followup_componenets.add_button(followup_componenets.BUTTON_STYLES.PRIMARY, 'Foo', 'button')

    followup.validate()


@pytest.mark.asyncio
async def test_followup_webhooks(mock_api):  # noqa: F811

    obj = Interaction().from_dict(samples.message_trigger_interaction)
    obj.generate_response()
    followup = obj.generate_followup()
    embeds = followup.add_embeds()
    embeds.generate('Test Embed')
    f_components = followup.add_components()
    f_components.add_button(f_components.BUTTON_STYLES.PRIMARY, 'my id', 'label')
    await followup._generate_webhook_data()


def test_response_methods(mock_api):  # noqa: F811

    obj = Interaction().from_dict(samples.message_trigger_interaction)
    response = obj.generate_response()
    response.add_choices()
    assert isinstance(response.data.choices, list)

    obj = Interaction().from_dict(samples.message_trigger_interaction)
    response = obj.generate_response()
    response.add_choice('Test', 'choice')
    assert isinstance(response.data.choices, list)


def test_response_validation(mock_api):  # noqa: F811

    obj = Interaction().from_dict(samples.message_trigger_interaction)
    response = obj.generate_response(Interaction.INTERACTION_RESPONSE_TYPES.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT)

    with pytest.raises(AttributeError):
        response.validate()

    response = InteractionResponse()
    with pytest.raises(AttributeError, match=r'Must have a type.'):
        response.validate()

    response.type = response.INTERACTION_RESPONSE_TYPES.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT
    for i in range(25):
        response.add_choice(str(i), i)

    response.validate()
    response.add_choice('last', 'straw')

    with pytest.raises(AttributeError, match=r'25 choices'):
        response.validate()
