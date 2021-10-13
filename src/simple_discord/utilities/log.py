import logging


class Log:

    log = logging.getLogger('simple-discord')
    log.setLevel(logging.INFO)
    _ch = logging.StreamHandler()
    _formatter = logging.Formatter('{asctime} - {levelname} - {filename}:{lineno} - {funcName} - {message}', style='{')
    _ch.setFormatter(_formatter)
    log.addHandler(_ch)

    def __getattr__(self, name):
        return getattr(self.log, name)
