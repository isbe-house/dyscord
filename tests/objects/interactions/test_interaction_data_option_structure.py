
import pytest
import copy

from src.dyscord.objects.interactions import Interaction, enumerations
from src.dyscord.objects import Channel, User
from . import samples


from ...fixtures import mock_api  # noqa: F401


def test_magics(mock_api):  # noqa: F811

    obj = Interaction().from_dict(samples.all_types)

    assert obj.data is not None
    assert isinstance(obj.data.options['channel'].value, Channel)
    assert 'channel' in obj.data.options

    obj = Interaction().from_dict(samples.nested_groups)

    assert obj.data is not None
    assert isinstance(obj.data.options['edit']['user']['target'].value, User)
    assert 'edit' in obj.data.options
    assert 'user' in obj.data.options['edit']
    assert 'target' in obj.data.options['edit']['user']


def test_invalid_from_dict(mock_api):  # noqa: F811

    data = copy.deepcopy(samples.nested_groups)

    # Add a value string, this will cause an error.
    data['data']['options'][0]['value'] = 'bad'

    with pytest.raises(ValueError):
        Interaction().from_dict(data)


def test_invalid_from_dict2(mock_api):  # noqa: F811

    data = copy.deepcopy(samples.nested_groups)

    # Add a value string, this will cause an error.
    data['data']['options'][0]['options'][0]['value'] = 'bad'

    with pytest.raises(ValueError):
        Interaction().from_dict(data)


def test_parsing(mock_api):  # noqa: F811

    data = copy.deepcopy(samples.all_types)

    Interaction().from_dict(data)


def test_parsing_deeply_nested(mock_api):  # noqa: F811

    data = copy.deepcopy(samples.all_types_nested)
    Interaction().from_dict(data)

    # We need to force the Member to be resolved, so delete users and reparse.
    del data['data']['resolved']['users']
    del data['data']['options'][0]['options'][0]['options'][1]
    Interaction().from_dict(data)


def test_all_mentionables(mock_api):  # noqa: F811
    data = copy.deepcopy(samples.all_types)

    for entry in data['data']['options']:
        if entry['type'] in [enumerations.COMMAND_OPTION.USER, enumerations.COMMAND_OPTION.CHANNEL, enumerations.COMMAND_OPTION.ROLE, enumerations.COMMAND_OPTION.MENTIONABLE]:
            entry['type'] = enumerations.COMMAND_OPTION.MENTIONABLE.value

    from pprint import pprint
    pprint(data)

    Interaction().from_dict(data)


def test_no_resolution_map(mock_api):  # noqa: F811
    data = copy.deepcopy(samples.all_types)

    del data['data']['resolved']
    with pytest.raises(ValueError):
        Interaction().from_dict(data)
