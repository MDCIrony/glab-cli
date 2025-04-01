"""
Logging configuration module for the GitLab API application.

This module provides a standardized logging setup that adapts to different
environments (development, testing, production). It configures loggers with
appropriate handlers, formatters and log levels based on the current environment.

Features:
    - Environment-based log level configuration
    - Console and file logging
    - Rotating file handler to manage log file sizes
    - Detailed formatting in development mode
    - Simplified formatting in production mode

Usage:

    logger = get_logger(__name__)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")


    Gets a configured logger based on the current environment.

        name (str): Name of the logger, typically __name__ of the module

        logging.Logger: A configured logger object

    Returns the current log level based on the ENVIRONMENT variable.

        int: The logging level constant (e.g., logging.DEBUG, logging.INFO)

    Returns the current environment name.

        str: The environment name ('development', 'testing', or 'production')
"""

import os
import logging
import logging.handlers
from pathlib import Path

ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

# Determine the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
LOGS_DIR = PROJECT_ROOT / "logs"

# Create logs directory if it doesn't exist
LOGS_DIR.mkdir(exist_ok=True)

# Define log levels for different environments
LOG_LEVELS = {
    "development": logging.DEBUG,
    "testing": logging.INFO,
    "production": logging.WARNING,
}

LOG_LEVEL = LOG_LEVELS.get(ENVIRONMENT, logging.INFO)

if ENVIRONMENT == "development":
    CONSOLE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    FILE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
else:
    CONSOLE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    FILE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": CONSOLE_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "file": {
            "format": FILE_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "console",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": LOG_LEVEL,
            "formatter": "file",
            "filename": LOGS_DIR / f"gitlab_api_{ENVIRONMENT}.log",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "": {  # Root logger
            "level": LOG_LEVEL,
            "handlers": (
                ["console", "file"] if ENVIRONMENT != "development" else ["console"]
            ),
            "propagate": True,
        }
    },
}


def get_logger(name):
    """Obtain a configured logger based on the current environment.

    Args:
        name (str): Name of the logger, typically __name__ of the module

    Returns:
        logging.Logger: A configured logger object
    """
    import logging.config

    logging.config.dictConfig(DEFAULT_CONFIG)

    logger = logging.getLogger(name)

    logger.debug(
        "Logger initialized with level %s for environment %s",
        logging.getLevelName(LOG_LEVEL),
        ENVIRONMENT,
    )

    return logger


def get_log_level():
    """Returns the current log level based on the ENVIRONMENT variable."""
    return LOG_LEVEL


def get_environment():
    """Returns the current environment name."""
    return ENVIRONMENT
