import pytest
import datetime

from src.dyscord.objects import Embed, EmbedAdder


@pytest.fixture
def blank_embed():
    return Embed()


def test_creation():
    x = Embed()
    assert type(x) is Embed


def test_add_fields(blank_embed: Embed):

    blank_embed.add_field('test', 'Bar')
    blank_embed.add_author('Brad', 'https://example.com/', 'https://example.com/test.png', 'https://cache.example.com/test.png')
    blank_embed.add_footer('Footer text', 'https://example.com/icon.jpeg', 'https://example.com/icon.jpeg')
    blank_embed.add_image('https://example.com/icon.jpeg', 'https://proxy.example.com/icon.jpeg', 500, 600)
    blank_embed.add_provider('Google', 'https://google.com/')
    blank_embed.add_thumbnail('https://example.com/icon.jpeg', 'https://proxy.example.com/icon.jpeg', 500, 600)
    blank_embed.add_video('https://example.com/icon.mp4', 'https://proxy.example.com/icon.mp4', 500, 600)

    now = datetime.datetime.now()

    blank_embed.generate(
        title='Test',
        type=blank_embed.EMBED_TYPES.rich,
        url='https://example.com/',
        color=0xFF00FF,
        description='Test description',
        timestamp=now,
    )

    blank_embed.validate()
    dict_output = blank_embed.to_dict()

    assert dict_output['title'] == 'Test'

    assert type(dict_output['fields']) is list
    assert dict_output['fields'][0]['name'] == 'test'
    assert dict_output['fields'][0]['value'] == 'Bar'
    assert dict_output['fields'][0]['inline'] is False

    assert type(dict_output['author']) is dict
    assert dict_output['author']['name'] == 'Brad'
    assert dict_output['author']['url'] == 'https://example.com/'
    assert dict_output['author']['icon_url'] == 'https://example.com/test.png'
    assert dict_output['author']['proxy_icon_url'] == 'https://cache.example.com/test.png'

    assert dict_output['type'] == 'rich'

    assert dict_output['url'] == 'https://example.com/'

    assert dict_output['color'] == 0xFF00FF

    assert dict_output['description'] == 'Test description'

    assert dict_output['timestamp'] == now.isoformat()


def test_invalids(blank_embed: Embed):
    pass


def test_basics(blank_embed: Embed):
    assert blank_embed.__str__() == 'Embed()'


def test_adder():

    class Foo(EmbedAdder):
        pass

    x = Foo()
    x.add_embeds()

    assert hasattr(x, 'embeds')
    assert type(x.embeds) is list
