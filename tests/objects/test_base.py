import pytest

from src.dyscord.objects.base_object import BaseDiscordObject


def test_instance():

    with pytest.raises(NotImplementedError):
        BaseDiscordObject()


def test_simply_child():

    class Child(BaseDiscordObject):
        pass

    obj = Child()
    assert isinstance(obj, Child)
    assert isinstance(obj, BaseDiscordObject)

    with pytest.raises(NotImplementedError):
        obj.to_dict()

    with pytest.raises(NotImplementedError):
        obj.from_dict({})

    with pytest.raises(NotImplementedError):
        obj._auto_dict({})


def test_simply_child2():
    class Child(BaseDiscordObject):
        _auto_map = {
            'test': [str, int]
        }

    with pytest.raises(IndexError):
        Child({'test': '1'})


def test_simply_child3():
    class Child(BaseDiscordObject):
        _auto_map = {
            'test': [str]
        }

    with pytest.raises(TypeError):
        Child({'test': '1'})
