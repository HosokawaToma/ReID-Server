import logging
from asyncio import Queue, Task
import asyncio
import abc

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


class BackgroundJob:
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    async def execute(self) -> str:
        pass


class BackgroundJobError(Exception):
    pass


class BackgroundQueue:
    _queue: Queue[BackgroundJob] = Queue()

    async def get(self) -> BackgroundJob:
        return await BackgroundQueue._queue.get()

    async def put(self, job: BackgroundJob) -> None:
        await BackgroundQueue._queue.put(job)


class BackgroundWorker:
    def __init__(
        self,
        logger: BackgroundLogger,
        queue: BackgroundQueue,
    ):
        self.logger = logger
        self.queue = queue
        self.task: Task | None = None

    async def start(self) -> None:
        self.task = asyncio.create_task(self.process())

    async def stop(self) -> None:
        if self.task:
            self.task.cancel()
            await self.task

    async def process(self) -> None:
        while True:
            try:
                job = await self.queue.get()
            except asyncio.CancelledError:
                break
            try:
                message = await job.execute()
                self.logger.info(f"Background job executed successfully: {job.name}: {message}")
            except BackgroundJobError as e:
                self.logger.error(f"Background job error: {job.name}: {e}. Skipping job.")
                continue
            except Exception as e:
                self.logger.error(f"Unexpected error processing background job: {job.name}: {e}")
                continue
