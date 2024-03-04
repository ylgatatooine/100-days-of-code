import logging
from __init__ import LOG_LEVEL, LOG_FILE

class Log:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(LOG_LEVEL)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)