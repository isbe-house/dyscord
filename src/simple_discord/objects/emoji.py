import emoji

from.base_object import BaseDiscordObject


class Emoji(BaseDiscordObject):

    def __init__(self, name: str = None, unicode: str = None):
        self.name = name
        self.unicode = unicode

        if (unicode is None) and (name is not None):
            assert type(self.name) is str
            self.unicode = emoji.unicode_codes.EMOJI_UNICODE_ENGLISH[self.name]

    def __str__(self):

        return f'Emoji(name={self.name}, unicode={self.unicode})'
