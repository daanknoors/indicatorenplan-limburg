# test_logging.py
import pytest
import os
import re
from pathlib import Path

from datetime import datetime
from indicatorenplan_limburg.system.logger import setup_logger
from indicatorenplan_limburg.configs.settings import PATH_REPO

def test_log_writes_to_file():
    log_dir = os.path.join(PATH_REPO, "logs")
    log_filename = os.path.join(log_dir, f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Setup logger
    log = setup_logger(log_dir=log_dir)
    log.info("Test log message")

    # Check if the log file was created
    assert os.path.exists(log_filename)

    # Check if the log file contains the test message
    with open(log_filename, 'r', encoding='utf-8') as file:
        content = file.read()
        assert re.search(r"Test log message", content) is not None

    # Clean up
    os.remove(log_filename)