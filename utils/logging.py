import logging
import logging.config
import os
from collections.abc import Callable


def apply_logging_conf() -> None:
    """
    Apply logging configuration
    """
    loglevel = os.environ.get("LOGLEVEL", "INFO").strip().upper()
    logtype = os.environ.get("LOGTYPE", "raw").strip().lower()

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "raw": {
                "format": "[%(asctime)s] %(levelname)s [%(threadName)s] %(message)s",
                "class": "logging.Formatter",
            },
        },
        "handlers": {
            "console": {
                "level": loglevel,
                "class": "logging.StreamHandler",
                "formatter": logtype,
            },
        },
        "loggers": {
            "uvicorn.access": {
                "propagate": False,
                "handlers": ["console"],
            },
            "uvicorn.error": {
                "propagate": False,
                "handlers": ["console"],
            },
        },
        "root": {
            "level": loglevel,
            "handlers": ["console"],
        },
    }

    logging.config.dictConfig(config)


def do_nothing(message, function, *args, **kwargs):
    pass


def get_debug_logger(logger: logging.Logger) -> Callable[[str, Callable, ...], None]:
    debug_enabled = logger.getEffectiveLevel() <= logging.DEBUG
    if debug_enabled is True:

        def logger_debug(message, function, *args, **kwargs):
            logger.debug(message.format(function(*args, **kwargs)))

        return logger_debug
    else:
        return do_nothing
