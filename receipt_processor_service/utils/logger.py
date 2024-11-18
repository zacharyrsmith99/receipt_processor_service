import os
import enum
from datetime import datetime

class LogLevel(enum.IntEnum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

class BaseLogger:
    def __init__(self, log_file_path):
        self.log_file_path = os.path.abspath(log_file_path)
        self.console_log_level = LogLevel[os.environ.get('CONSOLE_LOG_LEVEL', 'INFO')]
        self.write_log_level = LogLevel[os.environ.get('WRITE_LOG_LEVEL', 'INFO')]

    def set_log_level(self, level):
        if level in LogLevel.__members__:
            self.console_log_level = LogLevel[level]
        else:
            raise ValueError(f"Invalid log level: {level}")

    def _log(self, level, message):
        if LogLevel[level] >= self.console_log_level:
            timestamp = datetime.now().isoformat()
            log_message = f"{timestamp} [{level}] {message}\n"
            
            if LogLevel[level] >= self.write_log_level:
                with open(self.log_file_path, 'a') as log_file:
                    log_file.write(log_message)
            
            print(log_message, end='')

    def debug(self, message):
        self._log('DEBUG', message)

    def info(self, message):
        self._log('INFO', message)

    def warn(self, message):
        self._log('WARN', message)

    def error(self, message):
        self._log('ERROR', message)