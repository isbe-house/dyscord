import uuid
from unittest.mock import MagicMock

import pytest

from src.dyscord.objects.interactions import components
from src.dyscord.objects import Emoji
from src.dyscord.helper import CommandHandler


def test_action_row():

    def foo():
        pass

    emoji_mock = MagicMock(Emoji)

    assert isinstance(emoji_mock, Emoji)

    obj = components.ActionRow()

    button = obj.add_button(obj.BUTTON_STYLES.PRIMARY, emoji=emoji_mock, disabled=True, callback=foo, url='test_url')

    assert button.emoji == emoji_mock
    assert uuid.UUID(button.custom_id)
    assert button.disabled is True
    assert button.custom_id in CommandHandler.registered_custom_ids
    obj.to_dict()

    obj = components.ActionRow()

    menu = obj.add_select_menu(min_values=2, max_values=4, disabled=True, callback=foo)

    assert menu.min_values == 2
    assert menu.max_values == 4
    assert menu.disabled is True
    assert uuid.UUID(menu.custom_id)
    assert menu.custom_id in CommandHandler.registered_custom_ids
    obj.to_dict()


def test_button():
    obj = components.Button()
    obj.style = obj.BUTTON_STYLES.LINK
    with pytest.raises(AttributeError):
        obj.validate()
    obj.url = 123
    with pytest.raises(TypeError):
        obj.validate()
    obj.url = 'http://example.com'
    obj.validate()


def test_select_menu():
    obj = components.SelectMenu()
    obj.add_option_typed(obj.COMMAND_OPTION.INTEGER, 'Five', 'The number five')
    obj.placeholder = 'Foo'
    obj.validate()
    obj.to_dict()
