import uuid
import random

from src.dyscord.objects import Guild


def test_simple_guild():

    x = Guild()

    assert type(x) is Guild

    y = Guild()

    assert type(y) is Guild

    # Neither of these has an ID yet, they should be equal
    # TODO: Determine if this is something we wish to keep.
    # assert y == x


def test_dict_parsing():

    g1 = {
        'id': uuid.uuid4().int,
        'name': 'Test Server 1',
        'icon': str(uuid.uuid4()),
        'splash': str(uuid.uuid4()),
        'afk_channel_id': uuid.uuid4().int,
        'verification_level': random.randint(0, 4),
        'channels': [],
    }

    g2 = {
        'id': uuid.uuid4().int,
        'name': 'Test Server 2',
        'icon': str(uuid.uuid4()),
        'splash': str(uuid.uuid4()),
        'afk_channel_id': uuid.uuid4().int,
        'verification_level': random.randint(0, 4),
        'channels': [],
    }

    g1 = Guild().from_dict(g1)
    g2 = Guild().from_dict(g2)

    assert g1 != g2
