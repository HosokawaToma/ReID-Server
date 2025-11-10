import logging
import os
from entities.environment.storage import EntityEnvironmentStorage
from datetime import datetime
from errors.modules.logger import ErrorModuleLogger

class ModuleLogger:
    _logger: logging.Logger | None = None
    LOG_FILE_PATH = "{storage_path}/logs/{file_name}.log"

    def __init__(self, environment_storage: EntityEnvironmentStorage):
        self.path = self.LOG_FILE_PATH.format(
            storage_path=environment_storage.path,
            file_name=datetime.now().strftime("%Y%m%d%H%M%S")
        )
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if self._logger is None:
            self._logger = logging.getLogger()
            self._logger.setLevel(logging.INFO)
            self._logger.addHandler(logging.StreamHandler())
            self._logger.addHandler(logging.FileHandler(
                    self.path,
                )
            )

    def info(self, message: str):
        if self._logger is None:
            raise ErrorModuleLogger("Logger is not initialized")
        self._logger.info(message)

    def error(self, message: str):
        if self._logger is None:
            raise ErrorModuleLogger("Logger is not initialized")
        self._logger.error(message)

    def warning(self, message: str):
        if self._logger is None:
            raise ErrorModuleLogger("Logger is not initialized")
        self._logger.warning(message)

    def debug(self, message: str):
        if self._logger is None:
            raise ErrorModuleLogger("Logger is not initialized")
        self._logger.debug(message)
