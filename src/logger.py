import logging
from error import Error
import traceback
import datetime
import zoneinfo

class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(logging.FileHandler(f"{name}.log"))

    def unexpected_error(self, exception: Exception):
        self.logger.error(f"""Unexpected error: {exception.__class__.__name__}
    Timestamp: {datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).isoformat()}
    Traceback: {traceback.format_exc()}
"""
        )

    def error(self, error: Error):
        self.logger.error(f"""Error: {str(error)}
    Timestamp: {datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).isoformat()}
""")

    def info(self, message: str):
        self.logger.info(f"""Info: {message}
    Timestamp: {datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).isoformat()}
""")

    def api_request_info(self, request_id: str, request_path: str, request_method: str):
        self.logger.info(f"""API Request: id: {request_id}, path: {request_path}, method: {request_method}
    Timestamp: {datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).isoformat()}
""")

    def api_response_info(self, request_id: str, response_status_code: int):
        self.logger.info(f"""API Response: id: {request_id}, status: {response_status_code}
    Timestamp: {datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).isoformat()}
""")

    def background_info(self, background_id: str, name: str, message: str):
        self.logger.info(f"""Background: {message}
    ID: {background_id}
    Name: {name}
    Timestamp: {datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).isoformat()}
""")
