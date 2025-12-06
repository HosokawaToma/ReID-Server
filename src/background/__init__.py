import logging
import asyncio
import abc
import fastapi
import time


class BackgroundLogger:
    def __init__(self):
        self.logger = logging.getLogger("background")
        self.logger.setLevel(logging.INFO)
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


class BackgroundJobError(Exception):
    pass


class Background:
    def __init__(
        self,
        logger: BackgroundLogger,
    ):
        self.logger = logger
        self.task: asyncio.Task | None = None

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    def setup(self, app: fastapi.FastAPI):
        app.add_event_handler("startup", self.start)
        app.add_event_handler("shutdown", self.stop)

    async def start(self) -> None:
        self.task = asyncio.create_task(asyncio.to_thread(self.run))

    async def stop(self) -> None:
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                self.logger.error(
                    f"Unexpected error stopping background {self.name}: {e}")

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while True:
            try:
                message = loop.run_until_complete(self.process())
                self.logger.info(
                    f"Background {self.name} executed successfully: {message}")
            except BackgroundJobError as e:
                self.logger.error(
                    f"Background {self.name} error: {e}. Skipping job.")
                continue
            except Exception as e:
                self.logger.error(
                    f"Unexpected error processing background {self.name}: {e}")
                continue

    @abc.abstractmethod
    async def process(self) -> str:
        pass
