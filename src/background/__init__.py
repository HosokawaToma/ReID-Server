from logger import Logger
import asyncio
import abc
import fastapi
from error import Error
import threading
import uuid

class Background:
    def __init__(
        self,
        logger: Logger,
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
                self.logger.unexpected_error(e)

    async def run(self) -> None:
        while not self.event.is_set():
            try:
                background_id = str(uuid.uuid4())
                self.logger.background_info(
                    background_id=background_id,
                    name=self.name,
                    message="executing",
                )
                message = await asyncio.to_thread(self.handle)
                self.logger.background_info(
                    background_id=background_id,
                    name=self.name,
                    message=f"executed successfully: {message}",
                )
            except Error as e:
                self.logger.error(e)
                continue
            except Exception as e:
                self.logger.unexpected_error(e)
                continue

    @abc.abstractmethod
    def handle(self) -> str:
        pass
