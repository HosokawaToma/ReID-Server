import asyncio
from applications.identify_person.background.identify.queue import ApplicationIdentifyPersonBackgroundIdentifyQueue
from applications.identify_person.background.identify.processor import ApplicationIdentifyPersonBackgroundIdentifyProcessor
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
class ApplicationIdentifyPersonBackgroundIdentify:
    def __init__(
        self,
        queue: ApplicationIdentifyPersonBackgroundIdentifyQueue,
        processor: ApplicationIdentifyPersonBackgroundIdentifyProcessor,
    ):
        self.queue = queue
        self.processor = processor
        self.task: asyncio.Task[None] | None = None

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
    ):
        return cls(
            queue=ApplicationIdentifyPersonBackgroundIdentifyQueue(),
            processor=ApplicationIdentifyPersonBackgroundIdentifyProcessor.create(
                environment_postgresql=environment_postgresql,
            ),
        )

    async def start(self):
        self.task = asyncio.create_task(self.process())

    async def stop(self):
        if self.task is None:
            return
        self.task.cancel()
        self.task = None

    async def process(self):
        while True:
            try:
                id = await self.queue.get()
                await self.processor.process(id)
            except Exception as e:
                continue
