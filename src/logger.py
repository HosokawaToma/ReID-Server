import logging
from error import Error
import traceback

class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            self.logger.addHandler(logging.StreamHandler())
            self.logger.addHandler(logging.FileHandler(f"{name}.log"))

    def unexpected_error(self, exception: Exception, request_id: str | None = None):
        self.logger.error(f"""
Unexpected error:
    Request ID: {request_id}
    Class: {exception.__class__.__name__}
    Traceback: {traceback.format_exc()}
""")

    def error(self, error: Error, request_id: str | None = None):
        self.logger.error(f"""
Error:
    Request ID: {request_id}
    Message: {str(error)}
""")

    def info(self, message: str, request_id: str | None = None):
        self.logger.info(f"""
Info:
    Request ID: {request_id}
    Message: {message}
""")
