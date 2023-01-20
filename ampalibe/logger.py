import sys
import logging


class CustomFormatter(logging.Formatter):
    """
    Custom formatter for logging, add colors to the output and custom format
    """

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    green = "\x1b[32;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _format = "%(levelname)s|%(name)s:   %(message)s "

    # Define format of each status  (DEBUG|INFO|WARNINGS|ERROR|CRITICAL)
    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: green + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: bold_red + _format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def __logger(name="Ampalibe"):

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    # by default the logger will print on the console , in stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(CustomFormatter())
    log.addHandler(handler)
    return log


Logger = __logger()
