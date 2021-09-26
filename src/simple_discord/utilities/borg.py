from typing import Dict


class Borg:
    _shared_state: Dict[object, object] = {}

    def __init__(self):
        self.__dict__: Dict[object, object] = self._shared_state
