# import pytest

from src.simple_discord.client import DiscordClient


def test_simple_number_1():

    x = DiscordClient(token='1234')
    assert type(x) is DiscordClient
    assert 1 == 1
