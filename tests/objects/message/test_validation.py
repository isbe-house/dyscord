import pytest
import uuid

from src.simple_discord.objects import Message
from src.simple_discord.objects.interactions import BUTTON_STYLES


def test_bad_validation():

    x = Message()
    with pytest.raises(AssertionError):
        x.validate()

    x.content = 1234
    with pytest.raises(AssertionError):
        x.validate()

    x.content = 'Valid now'
    row = x.add_components()
    row.components = tuple()
    with pytest.raises(AssertionError):
        x.validate()

    row.components = list()
    row.components.append('This fails')
    with pytest.raises(AssertionError):
        x.validate()

    row.components = list()
    row.add_button(1, '1')
    with pytest.raises(AssertionError, match=r'Got invalid type'):
        x.validate()

    row.components = list()
    row.add_button(BUTTON_STYLES.PRIMARY, '1')
    with pytest.raises(AssertionError, match=r'Buttons in style.*must have a label'):
        x.validate()

    row.components = list()
    row.add_button(BUTTON_STYLES.PRIMARY, '1', label=123)
    with pytest.raises(AssertionError, match=r'Got invalid type .* of Button.label, must be str.'):
        x.validate()

    row.components = list()
    row.add_button(BUTTON_STYLES.PRIMARY, '1', label='1234', url='http://example.com')
    with pytest.raises(AssertionError, match=r'Cannot have url'):
        x.validate()

    row.components = list()
    row.add_button(BUTTON_STYLES.PRIMARY, '1', label='1234')
    row.add_button(BUTTON_STYLES.PRIMARY, '1', label='5678')
    with pytest.raises(AssertionError, match=r'Found duplicate custom_id'):
        x.validate()

    row.components = list()
    row.add_button(BUTTON_STYLES.PRIMARY, str(uuid.uuid4()), label='1')
    row.add_button(BUTTON_STYLES.PRIMARY, str(uuid.uuid4()), label='1')
    row.add_button(BUTTON_STYLES.PRIMARY, str(uuid.uuid4()), label='1')
    row.add_button(BUTTON_STYLES.PRIMARY, str(uuid.uuid4()), label='1')
    row.add_button(BUTTON_STYLES.PRIMARY, str(uuid.uuid4()), label='1')
    row.add_button(BUTTON_STYLES.PRIMARY, str(uuid.uuid4()), label='1')
    with pytest.raises(AssertionError, match=r'discord allows a max of 5'):
        x.validate()
