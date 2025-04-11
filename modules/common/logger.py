import logging
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent.parent.parent

def init_logger(filename):
    LOGGER = logging.getLogger(filename)
    LOGGER.setLevel(logging.INFO)
    handler = logging.FileHandler(CORE_DIR / f"data/{filename}.log", mode='a')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)

    return LOGGER
