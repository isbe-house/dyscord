import emoji

from.base_object import BaseDiscordObject


class Emoji(BaseDiscordObject):
    '''Emojis.'''

    def __init__(self, name: str = None, unicode: str = None):
        '''Initalize Emoji.

        TODO: Document parameters.
        '''
        self.name = name
        self.unicode = unicode

        if (unicode is None) and (name is not None):
            assert type(self.name) is str
            self.unicode = emoji.unicode_codes.EMOJI_UNICODE_ENGLISH[self.name]

    def __str__(self):
        '''Return string representation.'''
        return f'Emoji(name={self.name}, unicode={self.unicode})'
