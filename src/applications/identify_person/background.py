import asyncio
from asyncio import Queue
from typing import Optional
from entities.image import EntityImage
from modules.reid.model import ModuleReIDModel
from modules.storage.image import ModuleStorageImage
from modules.database.chroma.person_feature import ModuleDatabaseChromaPersonFeature
from entities.person_feature import EntityPersonFeature

class ApplicationIdentifyPersonBackgroundProcess:
    def __init__(
        self,
        reid_model: ModuleReIDModel,
        storage_image: ModuleStorageImage,
        database_person_feature: ModuleDatabaseChromaPersonFeature,
    ):
        self.reid_model = reid_model
        self.storage_image = storage_image
        self.database_person_feature = database_person_feature
        self.queue = Queue[EntityImage]()
        self.task: Optional[asyncio.Task[None]] = None

    async def start(self):
        self.task = asyncio.create_task(self.process_queue())

    async def stop(self):
        if self.task is not None:
            self.task.cancel()

    async def add(self, image: EntityImage):
        await self.queue.put(image)

    async def process_queue(self):
        while True:
            try:
                image = await self.queue.get()
                await self.process(image)
            except asyncio.CancelledError:
                break

    async def process(self, image: EntityImage) -> None:
        self.storage_image.save(image)
        query_feature = self.reid_model.extract_feature(image)
        self.database_person_feature.insert(EntityPersonFeature(
            feature=query_feature,
            camera_id=image.camera_id,
            view_id=image.view_id,
            timestamp=image.timestamp,
        ))
