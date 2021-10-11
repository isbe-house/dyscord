'''Components that can be attached to messages.'''

import abc
from typing import Dict, List, Union, Optional

from . import command, enumerations
from ..base_object import BaseDiscordObject
from .. import emoji


class Component(BaseDiscordObject):
    type: enumerations.COMPONENT_TYPES


class ComponentAdder(abc.ABC):
    '''Allow other objects to start adding components to themselves with a common set of helper functions.

    Caution: This is an abstract class, and is not intended for direct instantiation.
    '''

    def add_components(self) -> 'ActionRow':
        '''
        Start adding components by starting an ACTION_ROW.
        '''
        if not hasattr(self, 'components'):
            self.components: Optional[List['Component']] = list()
        assert type(self.components) is list
        new_action_row = ActionRow()
        self.components.append(new_action_row)

        return new_action_row


class ActionRow(Component):
    type = enumerations.COMPONENT_TYPES.ACTION_ROW
    components: List[Union['Button', 'SelectMenu']]

    def add_button(self,
                   style: enumerations.BUTTON_STYLES,
                   custom_id: Optional[str] = None,
                   label: Optional[str] = None,
                   emoji: Optional[emoji.Emoji] = None,
                   url: Optional[str] = None,
                   disabled: Optional[bool] = None,
                   ) -> 'Button':
        if not hasattr(self, 'components'):
            self.components = list()
        new_button = Button()
        new_button.style = style
        if label is not None:
            new_button.label = label
        if emoji is not None:
            new_button.emoji = emoji
        if custom_id is not None:
            new_button.custom_id = custom_id
        if url is not None:
            new_button.url = url
        if disabled is not None:
            new_button.disabled = disabled

        self.components.append(new_button)
        return new_button

    def add_select_menu(self,
                        custom_id: Optional[str] = None,
                        placeholder: Optional[str] = None,
                        min_values: Optional[int] = None,
                        max_values: Optional[int] = None,
                        disabled: Optional[bool] = None,
                        ) -> 'SelectMenu':
        if not hasattr(self, 'components'):
            self.components = list()
        new_select_menu = SelectMenu()
        if custom_id is not None:
            new_select_menu.custom_id = custom_id
        if placeholder is not None:
            new_select_menu.placeholder = placeholder
        if min_values is not None:
            new_select_menu.min_values = min_values
        if max_values is not None:
            new_select_menu.max_values = max_values
        if disabled is not None:
            new_select_menu.disabled = disabled

        self.components.append(new_select_menu)
        return new_select_menu

    def to_dict(self) -> dict:
        new_dict: Dict[str, object] = dict()
        new_dict['type'] = self.type.value
        new_dict['components'] = list()
        assert type(new_dict['components']) is list
        for component in self.components:
            new_dict['components'].append(component.to_dict())

        return new_dict

    def validate(self):
        if hasattr(self, 'components'):
            assert type(self.components) is list,\
                f'Got invalid type {type(self.components)} of ActionRow.components, must be list.'

            assert len(self.components) <= 5,\
                f'Found {len(self.components)} components, discord allows a max of 5.'

            for component in self.components:
                assert type(component) in [Button, SelectMenu],\
                    f'Got invalid type {type(component)} in ActionRow.components, must be Union[Button, SelectMenu].'
                component.validate()


class Button(Component):

    BUTTON_STYLES = enumerations.BUTTON_STYLES

    type = enumerations.COMPONENT_TYPES.BUTTON
    custom_id: str
    disabled: bool
    style: enumerations.BUTTON_STYLES
    label: str
    emoji: emoji.Emoji
    url: str

    def to_dict(self) -> dict:
        new_dict: Dict[str, object] = dict()
        new_dict['type'] = self.type.value
        if hasattr(self, 'custom_id'):
            new_dict['custom_id'] = self.custom_id
        if hasattr(self, 'disabled'):
            new_dict['disabled'] = self.disabled
        if hasattr(self, 'style'):
            new_dict['style'] = self.style
        if hasattr(self, 'label'):
            new_dict['label'] = self.label
        if hasattr(self, 'emoji'):
            new_dict['emoji'] = self.emoji
        if hasattr(self, 'url'):
            new_dict['url'] = self.url
        return new_dict

    def validate(self):
        assert self.type == enumerations.COMPONENT_TYPES.BUTTON,\
            f'Got invalid value {self.type} of Button.type, must be {enumerations.COMPONENT_TYPES.BUTTON}.'
        assert type(self.type) is enumerations.COMPONENT_TYPES,\
            f'Got invalid type {type(self.type)} of Button.type, must be {enumerations.COMPONENT_TYPES}.'

        assert hasattr(self, 'style'),\
            'A style must be set for Button.'
        assert type(self.style) is enumerations.BUTTON_STYLES,\
            f'Got invalid type {type(self.style)} of Button.style, must be {enumerations.BUTTON_STYLES}.'

        if self.style != enumerations.BUTTON_STYLES.LINK:
            assert hasattr(self, 'label'),\
                f'Buttons in style {self.style} must have a label.'
            assert type(self.label) is str,\
                f'Got invalid type {type(self.label)} of Button.label, must be str.'
            assert len(self.label) <= 80,\
                f'Got Button.label length of {len(self.label)}, max is 80.'
            assert len(self.label) >= 1,\
                f'Got Button.label length of {len(self.label)}, min is 1.'
            assert not hasattr(self, 'url'),\
                f'Cannot have url in a {self.style}.'
            assert hasattr(self, 'custom_id'),\
                'Button must have a custom_id.'
            assert type(self.custom_id) is str,\
                f'Got invalid type {type(self.custom_id)} of Button.custom_id, must be str.'
        else:
            assert hasattr(self, 'url'),\
                'Button must have URL when style is BUTTON_STYLES.LINK.'


class SelectMenu(Component):
    type = enumerations.COMPONENT_TYPES.SELECT_MENU
    custom_id: str
    disabled: bool
    options: List['command.CommandOptions']
    placeholder: str
    min_values: int
    max_values: int

    def add_option(self):  # -> 'command.CommandOptions':
        # TODO: Basically copy this in from our existing example.
        pass

    def to_dict(self) -> dict:
        new_dict: Dict[str, object] = dict()
        new_dict['type'] = self.type.value
        if hasattr(self, 'custom_id'):
            new_dict['custom_id'] = self.custom_id
        if hasattr(self, 'disabled'):
            new_dict['disabled'] = self.disabled
        if hasattr(self, 'options'):
            new_dict['options'] = list()
            assert type(new_dict['options']) is list
            for option in self.options:
                new_dict['options'].append(option.to_dict())
        if hasattr(self, 'placeholder'):
            new_dict['placeholder'] = self.placeholder
        if hasattr(self, 'min_values'):
            new_dict['min_values'] = self.min_values
        if hasattr(self, 'max_values'):
            new_dict['max_values'] = self.max_values
        return new_dict

    def validate(self):
        pass
