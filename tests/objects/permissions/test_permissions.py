import random
import pytest
from src.dyscord.objects import Permissions


def test_simple():
    bitfield = random.randint(0, (1 << 40) - 1)
    print(f'{bitfield:b}')
    x = Permissions(bitfield)
    assert type(x) is Permissions


def test_anding():
    bitfield = (1 << 40) - 1
    print(f'{bitfield:b}')
    x = Permissions(bitfield)
    assert type(x) is Permissions
    for permission in Permissions.PermissionFlags:
        assert permission in x.permissions
        assert permission & x

    x = Permissions(0b0101)
    y = Permissions(0b1010)
    assert (x & y) == Permissions()

    x = Permissions()
    for permission in Permissions.PermissionFlags:
        assert permission not in x.permissions
        assert not (permission & x)

    bitfield = random.randint(0, (1 << 40) - 1)
    x = Permissions(bitfield)
    y = Permissions(x)
    print(f'{bitfield:b}')
    print(x, y)
    assert x == y
    with pytest.raises(AssertionError):
        assert x != y


def test_inputs():

    # Good inputs
    Permissions()
    Permissions(0)
    Permissions('0')
    Permissions(0x1234)

    p1 = Permissions(0x12345)
    p2 = Permissions(p1)
    assert p1 & p2

    # Bad inputs
    with pytest.raises(ValueError):
        Permissions('')

    with pytest.raises(ValueError):
        Permissions('This is a bad input')

    with pytest.raises(ValueError):
        Permissions('0x1234')

    with pytest.raises(TypeError):
        Permissions(0.0)
