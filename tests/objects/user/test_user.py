import pytest

from src.dyscord.objects import User, Snowflake
from . import samples


def test_get_user_response():
    obj = User().from_dict(samples.raw_get_user_response)

    assert obj.id == Snowflake(samples.raw_get_user_response['id'])
    assert obj.username == 'Nelly'
    assert obj.discriminator == '1337'
    assert obj.avatar == '8342729096ea3675442027381ff50dfe'
    assert obj.verified is True
    assert obj.email == 'nelly@discord.com'
    assert obj.flags == 64
    assert obj.banner == '06c16474723fe537c283b8efa61a30c8'
    assert obj.premium_type == 1
    assert obj.public_flags == 64


def test_magics():
    obj1 = User().from_dict(samples.raw_get_user_response)
    obj2 = User().from_dict(samples.raw_get_user_response)

    # Check to make sure __repr__ is covered
    print([obj1, obj2])

    assert obj1 == obj2

    with pytest.raises(NotImplementedError):
        obj1 == 1

    assert obj1.mention == f'<@{samples.raw_get_user_response["id"]}>'
