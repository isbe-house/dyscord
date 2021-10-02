import pytest
import datetime

from src.simple_discord.objects import Embed


@pytest.fixture
def blank_embed():
    return Embed()


def test_creation():
    x = Embed()
    assert type(x) is Embed


def test_add_fields(blank_embed: Embed):

    blank_embed.add_field('test', 'Bar')

    blank_embed.generate('Test', timestamp=datetime.datetime.now())

    blank_embed.validate()
    dict_output = blank_embed.to_dict()

    assert dict_output['title'] == 'Test'
    assert type(dict_output['fields']) is list
    assert dict_output['fields'][0]['name'] == 'test'
    assert dict_output['fields'][0]['value'] == 'Bar'
    assert dict_output['fields'][0]['inline'] is False


def test_invalids(blank_embed: Embed):
    pass
