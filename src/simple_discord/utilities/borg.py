'''Borg design module.'''
from typing import Dict


class Borg:
    '''Borg design pattern base class.'''

    _shared_state: Dict[object, object] = {}

    def __init__(self):
        '''To be called by child-classes.'''
        self.__dict__: Dict[object, object] = self._shared_state
