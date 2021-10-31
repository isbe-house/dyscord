'''Collection of events which are less likely to be directly implemented by the end user.'''

from .typing_start import TypingStart
from .guild_member_update import GuildMemberUpdate
from .voice_state import VoiceState


__all__ = [
    'GuildMemberUpdate',
    'TypingStart',
    'VoiceState'
]
