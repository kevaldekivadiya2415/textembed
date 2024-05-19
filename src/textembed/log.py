"""Module used for logging"""

import logging
import sys
from enum import Enum
from typing import Any

# Clear any existing handlers to avoid duplicate log messages
logging.getLogger().handlers.clear()

# Initialize a list to hold logging handlers
log_handlers: list[Any] = []

# Try to import RichHandler from rich library
try:
    from rich.console import Console
    from rich.logging import RichHandler

    # If successful, append RichHandler to handlers list
    rich_handler = RichHandler(console=Console(stderr=True), show_time=False)
    log_handlers.append(rich_handler)
except ImportError:
    # If import fails, append StreamHandler to handlers list
    log_handlers.append(logging.StreamHandler(sys.stderr))

# Define log levels
LOG_LEVELS: dict[str, int] = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "trace": 5,
}

# Define log format
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s: %(message)s"

# Configure root logger with default level, format, and handlers
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=log_handlers,
)

# Get logger instance for "textembed" namespace
logger = logging.getLogger("textembed")


# Define an Enum for uvicorn log levels
class UvicornLogLevels(Enum):
    """Uvicorn log levels

    Args:
        Enum (str): Enum

    Returns:
        str: Log levels
    """

    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    TRACE = "trace"
