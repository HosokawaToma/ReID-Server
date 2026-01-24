import logging
from error import Error
from types import TracebackType
import traceback
import datetime
import zoneinfo

class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(logging.FileHandler(f"{name}.log"))

    def _traceback(self, exc_traceback: TracebackType):
        stack_summary = traceback.extract_tb(exc_traceback)
        return "->\n".join([f"{summary.filename}:{summary.lineno}:{summary.name}" for summary in stack_summary])

    def _timestamp(self):
        return datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).isoformat()

    def unexpected_error(self, exception: Exception, id: str):
        self.logger.error(f"""Unexpected error: id: {id}
    Error: {exception.__class__.__name__} -> {str(exception)}
    Timestamp: {self._timestamp()}
    Traceback: {self._traceback(exception.__traceback__) if exception.__traceback__ is not None else None}
"""
        )

    def error(self, error: Error, id: str):
        self.logger.error(f"""Error: id: {id}
    Error: {error.__class__.__name__} -> {error.message}
    Timestamp: {self._timestamp()}
    Traceback: {self._traceback(error.__traceback__) if error.__traceback__ is not None else None}
""")

    def api_request_info(self, request_id: str, request_path: str, request_method: str):
        self.logger.info(f"""API Request: id: {request_id}, path: {request_path}, method: {request_method}
    Timestamp: {self._timestamp()}
""")

    def api_response_info(self, request_id: str, response_status_code: int):
        self.logger.info(f"""API Response: id: {request_id}, status: {response_status_code}
    Timestamp: {self._timestamp()}
""")

    def background_info(self, process_id: str, name: str, message: str):
        self.logger.info(f"""Background: id: {process_id}, name: {name}, message: {message}
    Timestamp: {self._timestamp()}
""")
