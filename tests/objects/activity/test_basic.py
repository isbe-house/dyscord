from src.dyscord.objects import Activity, enumerations

from . import samples


def test_init():
    obj = Activity()

    assert isinstance(obj, Activity)


def test_simply_activity():
    data = samples.simple_activity
    obj = Activity(data)

    assert obj.details == data['details']
    assert obj.state == data['state']
    assert obj.name == data['name']
    assert obj.type == data['type']
    assert isinstance(obj.type, enumerations.ACTIVITY_TYPE)
    assert isinstance(obj.type, int)
    assert obj.url == data['url']


def test_rich_activity():
    data = samples.rich_presense_activity
    obj = Activity(data)

    assert obj.name == data['name']
    assert obj.type == data['type']
    assert isinstance(obj.type, enumerations.ACTIVITY_TYPE)
    assert isinstance(obj.type, int)
    assert obj.application_id == data['application_id']
    assert obj.state == data['state']
    assert obj.details == data['details']
    assert obj.timestamps is not None
    assert obj.party is not None
    assert obj.assets is not None
    assert obj.secrets is not None
    assert obj.buttons is not None
    assert isinstance(obj.buttons, list)
    assert obj.emoji is not None
