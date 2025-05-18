import logging
import os
from functools import wraps


def setup_logging():
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    logger.handlers.clear()  # Cache handling of logger instances

    # Console handler (for live viewing)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)

    # File handler (for persistent logs)
    os.makedirs("docs/logging", exist_ok=True)
    file_handler = logging.FileHandler('docs/logging/debug.log')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def debug_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        if logger.isEnabledFor(logging.DEBUG):
            if args and hasattr(args[0], func.__name__):  # for classes
                args_repr = [repr(arg) for arg in args[1:]]  # skips the first arg -> self
                class_or_instance = args[0].__class__.__name__  # Get class name
                logger.debug(f"{class_or_instance}, {func.__name__}, args: {args_repr}, kwargs: {kwargs}")
            else:  # for standalone functions
                logger.debug(f"{func.__qualname__} - args: {args}, kwargs: {kwargs})")
        return func(*args, **kwargs)

    return wrapper
