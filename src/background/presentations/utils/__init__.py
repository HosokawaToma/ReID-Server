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
                self.logger.unexpected_error(exception=e, id=self.name)

    async def run(self) -> None:
        while not self.event.is_set():
            process_id = str(uuid.uuid4())
            try:
                self.logger.background_info(
                    process_id=process_id,
                    name=self.name,
                    message=f"background started",
                )
                await asyncio.to_thread(self.handle, process_id=process_id)
                self.logger.background_info(
                    process_id=process_id,
                    name=self.name,
                    message=f"background finished",
                )
            except Error as e:
                self.logger.error(error=e, id=process_id)
                continue
            except Exception as e:
                self.logger.unexpected_error(exception=e, id=process_id)
                continue

    @abstractmethod
    def handle(self, process_id: str) -> None:
        pass
