import logging

class PresentationLogger:
    def __init__(self):
        self.logger = logging.getLogger("presentation")

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)
