import logging
import os
from datetime import datetime

from config import LOG_FOLDER


def setup_logger():

    today = datetime.now().strftime("%Y-%m-%d")

    log_directory = os.path.join(LOG_FOLDER, today)

    os.makedirs(log_directory, exist_ok=True)

    log_file = os.path.join(
        log_directory,
        "automation.log"
    )

    logger = logging.getLogger("CollectionAutomation")

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)

    return logger


logger = setup_logger()