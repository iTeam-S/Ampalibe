import sys
import logging


class Logger:
    """
    Logger class for Ampalibe, by default the logger name is Ampalibe
    """

    def __init__(self, name="Ampalibe"):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        format_ = CustomFormatter()

        # by default the logger will print on the console , in stdout
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(format_)
        logger.addHandler(handler)

        self.logger = logger


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
    format_ = "%(levelname)s|%(name)s:   %(message)s "

    # Define format of each status  (DEBUG|INFO|WARNINGS|ERROR|CRITICAL)
    FORMATS = {
        logging.DEBUG: grey + format_ + reset,
        logging.INFO: green + format_ + reset,
        logging.WARNING: yellow + format_ + reset,
        logging.ERROR: red + format_ + reset,
        logging.CRITICAL: bold_red + format_ + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
