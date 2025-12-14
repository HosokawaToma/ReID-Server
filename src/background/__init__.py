import logging
import asyncio
import abc
import fastapi
from error import Error
import threading
import traceback
class BackgroundLogger:
    def __init__(self):
        self.logger = logging.getLogger("background")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            self.logger.addHandler(logging.StreamHandler())
            self.logger.addHandler(logging.FileHandler("background.log"))


    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)


class BackgroundJobError(Error):
    pass


class Background:
    def __init__(
        self,
        logger: BackgroundLogger,
    ):
        self.logger = logger
        self.task: asyncio.Task | None = None
        self.event = threading.Event()
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    def setup(self, app: fastapi.FastAPI):
        app.add_event_handler("startup", self.start)
        app.add_event_handler("shutdown", self.stop)

    async def start(self) -> None:
        self.task = asyncio.create_task(self.run())
        self.event.clear()

    async def stop(self) -> None:
        if self.task:
            self.event.set()
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                self.logger.error(
                    f"Unexpected error stopping background {self.name}: {e}")

    async def run(self) -> None:
        while not self.event.is_set():
            try:
                message = await asyncio.to_thread(self.handle)
                self.logger.info(
                    f"Background {self.name} executed successfully: {message}")
            except BackgroundJobError as e:
                self.logger.error(f"Background {self.name} error: {e.message}")
                continue
            except Exception as e:
                self.logger.error(
                    f"Unexpected error processing background {self.name}: {traceback.format_exc()}")
                continue

    @abc.abstractmethod
    def handle(self) -> str:
        pass
