from applications.identify_person.background.feature.queue import ApplicationIdentifyPersonBackgroundFeatureQueue
from applications.identify_person.background.feature.processor import ApplicationIdentifyPersonBackgroundFeatureProcessor
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from entities.environment.storage import EntityEnvironmentStorage
import asyncio
import logging

class ApplicationIdentifyPersonBackgroundFeature:
    def __init__(
        self,
        queue: ApplicationIdentifyPersonBackgroundFeatureQueue,
        processor: ApplicationIdentifyPersonBackgroundFeatureProcessor
    ):
        self.queue = queue
        self.processor = processor
        self.task: asyncio.Task[None] | None = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(logging.FileHandler("identify_person_background_feature.log"))

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
        environment_storage: EntityEnvironmentStorage,
    ):
        return cls(
            queue=ApplicationIdentifyPersonBackgroundFeatureQueue(),
            processor=ApplicationIdentifyPersonBackgroundFeatureProcessor.create(
                environment_postgresql=environment_postgresql,
                environment_storage=environment_storage,
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
                id, callback = await self.queue.get()
                self.logger.info(f"Processing feature for image {id}")
                person_feature = await self.processor.process(id)
                if callback is not None:
                    await callback(person_feature.id)
                self.logger.info(f"Feature processed for image {id}")
            except Exception as e:
                continue
