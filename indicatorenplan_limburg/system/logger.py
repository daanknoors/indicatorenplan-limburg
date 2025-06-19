"""Set up a logger for the metrics module."""
import logging
import os
from datetime import datetime

from indicatorenplan_limburg.configs.settings import PATH_REPO


def setup_logger(name="indicatorenplan-limburg", log_dir=None, level='INFO'):
    log = logging.getLogger(name)

    # Check if the logger already has handlers, only configure once
    if log.hasHandlers():
        return log

    # Use the project repository's logs directory if no log_dir is provided
    if log_dir is None:
        log_dir = os.path.join(PATH_REPO, "logs")

    # Ensure log directory exists
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create log directory: {log_dir}. Error: {e}")

    # Timestamped log filename
    log_filename = os.path.join(
        log_dir,
        f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    # File handler logs everything
    try:
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
    except Exception as e:
        raise RuntimeError(f"Failed to create log file: {log_filename}. Error: {e}")

    # Console handler logs info and up
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatters
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    log.addHandler(file_handler)
    log.addHandler(console_handler)
    if level is not None:
        log.setLevel(level)
    # Ensure logs bubble up to shared_logger
    log.propagate = True

    # Debugging output
    log.debug(f"Logger initialized. Log file: {log_filename}")

    return log
