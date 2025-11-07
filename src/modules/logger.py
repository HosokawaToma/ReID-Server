import logging
from entities.environment.storage import EntityEnvironmentStorage
from datetime import datetime

class ModuleLogger:
    _logger: logging.Logger
    LOG_FILE_PATH = "{storage_path}/logs/{file_name}.log"

    def __init__(self, environment_storage: EntityEnvironmentStorage):
        if self._logger is None:
            self._logger = logging.getLogger()
            self._logger.setLevel(logging.INFO)
            self._logger.addHandler(logging.StreamHandler())
            self._logger.addHandler(logging.FileHandler(
                    self.LOG_FILE_PATH.format(
                        storage_path=environment_storage.path,
                        file_name=datetime.now().strftime("%Y%m%d%H%M%S")
                    ),
                )
            )

    def info(self, message: str):
        self._logger.info(message)

    def error(self, message: str):
        self._logger.error(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def debug(self, message: str):
        self._logger.debug(message)
