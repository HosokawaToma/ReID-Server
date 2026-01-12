from logger import Logger
import asyncio
from abc import ABC, abstractmethod
from error import Error
import threading
import uuid

class BackgroundPresentationUtilsBase(ABC):
    def __init__(
        self,
        logger: Logger,
    ):
        self.logger = logger
        self.task: asyncio.Task | None = None
        self.event = threading.Event()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

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
                    message=f"background started",
                )
                await asyncio.to_thread(self.handle, background_id=background_id)
                self.logger.background_info(
                    background_id=background_id,
                    name=self.name,
                    message=f"background finished",
                )
            except Error as e:
                self.logger.error(e)
                continue
            except Exception as e:
                self.logger.unexpected_error(e)
                continue

    @abstractmethod
    def handle(self, background_id: str) -> None:
        pass
