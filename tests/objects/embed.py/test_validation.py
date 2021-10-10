import pytest

from src.simple_discord.objects import Embed


@pytest.fixture
def blank_embed():
    return Embed()


def test_title(blank_embed: Embed):

    blank_embed.generate(title='X' * 257)
    with pytest.raises(AssertionError):
        blank_embed.validate()

    blank_embed.generate(title='X' * 256)
    blank_embed.validate()


def test_description(blank_embed: Embed):

    blank_embed.generate(title='X', description='X' * 4097)
    with pytest.raises(AssertionError):
        blank_embed.validate()

    blank_embed.generate(title='X', description='X' * 4096)
    blank_embed.validate()


def test_fields(blank_embed: Embed):

    blank_embed.generate(title='X', description='X')
    for i in range(26):
        blank_embed.add_field(f'{i}', f'{i}')
    with pytest.raises(AssertionError):
        blank_embed.validate()

    del blank_embed.fields
    for i in range(25):
        blank_embed.add_field(f'{i}', f'{i}')
    blank_embed.validate()

    del blank_embed.fields
    blank_embed.add_field('X' * 257, 'X')
    with pytest.raises(AssertionError):
        blank_embed.validate()
    del blank_embed.fields
    blank_embed.add_field('X' * 255, 'X')
    blank_embed.validate()

    del blank_embed.fields
    blank_embed.add_field('X', 'X' * 1025)
    with pytest.raises(AssertionError):
        blank_embed.validate()
    del blank_embed.fields
    blank_embed.add_field('X', 'X' * 1024)
    blank_embed.validate()


def test_footer(blank_embed: Embed):
    blank_embed.add_footer('X' * 2049)
    with pytest.raises(AssertionError):
        blank_embed.validate()
    blank_embed.add_footer('X' * 2048)
    blank_embed.validate()


def test_hidden(blank_embed: Embed):
    blank_embed.generate('X' * 256, description='X' * 4096)
    for i in range(25):
        blank_embed.add_field('X' * 256, 'X' * 1024)
    with pytest.raises(AssertionError):
        blank_embed.validate()
