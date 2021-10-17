
import emoji
from src.dyscord.objects import Emoji


def test_basic_emoji():

    x = Emoji()

    print(x)


def test_all_emoji():

    for e in emoji.unicode_codes.EMOJI_UNICODE_ENGLISH:
        print(e)


def test_all_emoji_as_objects():

    for e in emoji.unicode_codes.EMOJI_UNICODE_ENGLISH:
        e = Emoji(e)
