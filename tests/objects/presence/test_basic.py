from src.dyscord.objects import Presence

from . import samples


def test_init():
    obj = Presence()
    assert isinstance(obj, Presence)


def test_basic_sample():
    data = samples.simple_presence
    obj = Presence(data)

    assert isinstance(obj, Presence)
    assert obj.user.id == data['user']['id']
