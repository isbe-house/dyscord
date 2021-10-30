'''Collection of events which are less likely to be directly implemented by the end user.'''

from .typing_start import TypingStart
from .guild_member_update import GuildMemberUpdate


__all__ = [
    'TypingStart',
    'GuildMemberUpdate',
]
