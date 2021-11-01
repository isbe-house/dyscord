
import pytest

from src.dyscord.objects.interactions.interaction import InteractionCallback


def test_basics():

    obj = InteractionCallback()
    obj.generate(ephemeral=True)
    obj.tts = True
    obj.content = 'Foo'
    embeds = obj.add_embeds()
    embeds.generate('Test title')

    components = obj.add_components()
    components.add_button(components.BUTTON_STYLES.PRIMARY, 'my id', 'label')

    obj.to_dict()

    # Need to show that we can use an int here.
    obj.flags = 8
    obj.to_dict()

    obj = InteractionCallback()
    obj.add_choice('test', 'choice')
    obj.to_dict()

    obj.flags = 'WRONG'

    with pytest.raises(TypeError):
        obj.to_dict()


def test_generate():

    obj = InteractionCallback()
    obj.generate(ephemeral=True)
    assert obj.flags & obj.INTERACTION_CALLBACK_FLAGS.EPHEMERAL

    obj = InteractionCallback()
    obj.generate(ephemeral=False)
    assert not (obj.flags & obj.INTERACTION_CALLBACK_FLAGS.EPHEMERAL)


def test_validation():

    obj = InteractionCallback()
    obj.add_choices()
    obj.tts = True
    with pytest.raises(AttributeError, match=r'tts'):
        obj.validate()

    obj = InteractionCallback()
    obj.add_choices()
    obj.content = 'test'
    with pytest.raises(AttributeError, match=r'content'):
        obj.validate()

    obj = InteractionCallback()
    obj.add_choices()
    obj.add_embeds()
    with pytest.raises(AttributeError, match=r'embeds'):
        obj.validate()

    obj = InteractionCallback()
    obj.add_choices()
    obj.generate(ephemeral=True)
    with pytest.raises(AttributeError, match=r'flags'):
        obj.validate()

    obj = InteractionCallback()
    obj.add_choices()
    obj.add_components()
    with pytest.raises(AttributeError, match=r'components'):
        obj.validate()
