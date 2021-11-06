from logging_levels.standards import add_standards  # type: ignore
import logging
add_standards(logging)


class Log:
    '''Generalized logging class for easy import.

    Attributes:
        trace: 5
        verbose: 7
        debug: 10
        info: 20
        notice: 25
        warning: 30
        suppressed: 31
        error: 40
        critical: 50
        alert: 70
        emergency: 100
        exception: ?
    '''

    log = logging.getLogger('dyscord')
    log.setLevel(logging.INFO)
    _ch = logging.StreamHandler()
    _formatter = logging.Formatter('{asctime} - {levelname} - {filename}:{lineno} - {funcName} - {message}', style='{')
    _ch.setFormatter(_formatter)
    log.addHandler(_ch)

    def __getattr__(self, name):
        '''Map in the logging class attributes.'''
        return getattr(self.log, name)

    trace = log.trace  # type: ignore
    verbose = log.verbose  # type: ignore
    debug = log.debug
    info = log.info
    notice = log.notice  # type: ignore
    warning = log.warning
    suppressed = log.suppressed  # type: ignore
    error = log.error
    critical = log.critical
    alert = log.alert  # type: ignore
    emergency = log.emergency  # type: ignore
    exception = log.exception
