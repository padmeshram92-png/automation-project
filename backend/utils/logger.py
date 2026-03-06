import logging
import os

LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(LOG_FOLDER, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_info(message):
    """Log an info level message"""
    logging.info(message)


def log_error(message):
    """Log an error level message"""
    logging.error(message)


def log_warning(message):
    """Log a warning level message"""
    logging.warning(message)
