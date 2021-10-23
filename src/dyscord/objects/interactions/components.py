'''Components that can be attached to messages.'''

import abc
import uuid
from typing import Callable, Dict, List, Union, Optional

from . import command, enumerations
from ..base_object import BaseDiscordObject
from .. import emoji
from ...helper import command_handler


class Component(BaseDiscordObject, abc.ABC):
    '''Base class for Components.'''
    type: enumerations.COMPONENT_TYPES


class ComponentAdder(abc.ABC):
    '''Allow other objects to start adding components to themselves with a common set of helper functions.

    Caution: This is an abstract class, and is not intended for direct instantiation.
    '''

    def add_components(self) -> 'ActionRow':
        '''Start adding components by starting an ACTION_ROW.'''
        if not hasattr(self, 'components') or self.components is None:
            self.components: Optional[List['Component']] = list()
        assert type(self.components) is list
        new_action_row = ActionRow()
        self.components.append(new_action_row)

        return new_action_row


class ActionRow(Component):
    '''Intermediate Component that holds Button or SelectMenu objects.'''
    type = enumerations.COMPONENT_TYPES.ACTION_ROW
    components: List[Union['Button', 'SelectMenu']]

    BUTTON_STYLES = enumerations.BUTTON_STYLES

    def add_button(self,
                   style: enumerations.BUTTON_STYLES,
                   custom_id: Optional[str] = None,
                   label: Optional[str] = None,
                   emoji: Optional[emoji.Emoji] = None,
                   url: Optional[str] = None,
                   disabled: Optional[bool] = None,
                   callback: Callable = None,
                   unlimited_callbacks: bool = False,
                   ) -> 'Button':
        '''Append a Button item to the ActionRow, and return it.

        Arguments:
            style (BUTTON_STYLES): Style of button to be used.
            custom_id (str): Unique string to be returned by the API when item is selected. Default is UUID4.
            label (str): Actual text user will see.
            emoji (Emoji): Emoji rather than label to display.
            url: (str): URL for BUTTON_STYLES.LINK buttons.
            disabled (bool): Item will display, but is not interactable.
            callback (Callable): Callback function when user selects an item. Should be
            unlimited_callbacks (bool): Request callbacks even if custom_id has already been called.

        Returns:
            Button
        '''
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
        elif custom_id is None and style != enumerations.BUTTON_STYLES.LINK:
            new_button.custom_id = str(uuid.uuid4())
        if url is not None:
            new_button.url = url
        if disabled is not None:
            new_button.disabled = disabled

        self.components.append(new_button)

        if callback is not None:
            command_handler.CommandHandler.register_interaction_custom_id(
                new_button.custom_id,
                callback,
                unlimited_callbacks,
            )

        return new_button

    def add_select_menu(self,
                        custom_id: Optional[str] = None,
                        placeholder: Optional[str] = None,
                        min_values: Optional[int] = None,
                        max_values: Optional[int] = None,
                        disabled: Optional[bool] = None,
                        callback: Callable = None,
                        unlimited_callbacks: bool = False,
                        ) -> 'SelectMenu':
        '''Append a SelectMenu item to the ActionRow, and return it.

        Arguments:
            custom_id (str): Unique string to be returned by the API when item is selected. Default is UUID4.
            placeholder (str): Text to appear in the box before user selection begins.
            min_values (int): Min number of items user must select. Default is 1.
            max_values (int): Max number of items user can select. Default is 1.
            disabled (bool): Item will display, but is not interactable.
            callback (Callable): Callback function when user selects an item. Should be
            unlimited_callbacks (bool): Request callbacks even if custom_id has already been called.

        Returns:
            SelectMenu
        '''
        if not hasattr(self, 'components'):
            self.components = list()
        new_select_menu = SelectMenu()
        if custom_id is not None:
            new_select_menu.custom_id = custom_id
        else:
            new_select_menu.custom_id = str(uuid.uuid4())
        if placeholder is not None:
            new_select_menu.placeholder = placeholder
        if min_values is not None:
            new_select_menu.min_values = min_values
        if max_values is not None:
            new_select_menu.max_values = max_values
        if disabled is not None:
            new_select_menu.disabled = disabled

        self.components.append(new_select_menu)

        if callback is not None:
            command_handler.CommandHandler.register_interaction_custom_id(
                new_select_menu.custom_id,
                callback,
                unlimited_callbacks,
            )

        return new_select_menu

    def to_dict(self) -> dict:
        '''Convert object to dictionary suitable for API or other generic useage.'''
        new_dict: Dict[str, object] = dict()
        new_dict['type'] = self.type.value
        new_dict['components'] = list()
        assert type(new_dict['components']) is list
        for component in self.components:
            new_dict['components'].append(component.to_dict())

        return new_dict

    def validate(self):
        '''Validate object is prepared for dispatch to discord.'''
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
    '''Selectable button or link for user interaction.'''

    BUTTON_STYLES = enumerations.BUTTON_STYLES

    type = enumerations.COMPONENT_TYPES.BUTTON
    custom_id: str
    disabled: bool
    style: enumerations.BUTTON_STYLES
    label: str
    emoji: emoji.Emoji
    url: str

    def to_dict(self) -> dict:
        '''Convert object to dictionary suitable for API or other generic useage.'''
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
        '''Validate object is prepared for dispatch to discord.'''
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
    '''A drop down menu for user interaction.'''

    type = enumerations.COMPONENT_TYPES.SELECT_MENU
    custom_id: str
    disabled: bool
    options: List['command.CommandOptions']
    placeholder: str
    min_values: int
    max_values: int

    add_option_typed = command.Command.add_option_typed

    def to_dict(self) -> dict:
        '''Convert object to dictionary suitable for API or other generic useage.'''
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
        '''Validate object is prepared for dispatch to discord.'''
        pass
