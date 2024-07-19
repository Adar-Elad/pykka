
TERMINAL_COLOR = {
    'yellow': '\033[93m',
    'reset':  '\033[00m',
    'blue':   '\033[94m',
    'cyan':   '\033[96m',
}


class Logger:
    # ==> Logger severity levels
    SEVERITY = {
        'debug': 0,
        'info':  1,
        'warn':  2,
        'error': 3
    }

    def __init__(self, title, severity=None):
        self.level = severity if severity else self.SEVERITY['debug']
        self.title = title

    def set_level(self, level):
        self.level = level

    def pp(self, title, severity, msg, error=False):
        if self.level >= self.SEVERITY[severity]:
            print(f"{TERMINAL_COLOR['blue']}"
                        f"{title}"
                  f"{TERMINAL_COLOR['reset']}"
                  f" :: {TERMINAL_COLOR['red' if severity == 'error' else 'yellow']}"
                        f"{severity.upper()}"
                  f"{TERMINAL_COLOR['reset']}"
                  f" :: {TERMINAL_COLOR['red' if severity == 'error' else 'cyan']}"
                        f"{msg}"
                  f"{TERMINAL_COLOR['reset']}")

    def debug(self, msg):
        self.pp(title=self.title, severity='debug', msg=msg)

    def info(self, msg):
        self.pp(title=self.title, severity='info', msg=msg)

    def warn(self, msg):
        self.pp(title=self.title, severity='warn', msg=msg)

    def error(self, msg):
        self.pp(title=self.title, severity='error', msg=msg)

