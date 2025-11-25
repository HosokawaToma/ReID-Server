import uuid
from queue import Queue
from typing import Callable
from dataclasses import dataclass
import fastapi

from applications.person.feature.creator import ApplicationPersonFeatureCreator
from applications.person.image import ApplicationPersonImage
from applications.person.image import ApplicationPersonImageSearchFilters
from presentation import PresentationLogger

class PresentationBackgroundPersonFeatureCreateQueueError(Exception):
    pass

@dataclass
class PresentationBackgroundPersonFeatureCreateQueueItem:
    person_image_id: uuid.UUID
    callback: Callable[[uuid.UUID], None] | None = None

class PresentationBackgroundPersonFeatureCreateQueue():
    _queue: Queue[PresentationBackgroundPersonFeatureCreateQueueItem] | None = None

    def __init__(self):
        if PresentationBackgroundPersonFeatureCreateQueue._queue is None:
            PresentationBackgroundPersonFeatureCreateQueue._queue = Queue[PresentationBackgroundPersonFeatureCreateQueueItem]()

    def get(self) -> PresentationBackgroundPersonFeatureCreateQueueItem:
        if PresentationBackgroundPersonFeatureCreateQueue._queue is None:
            raise PresentationBackgroundPersonFeatureCreateQueueError("Queue not initialized")
        return PresentationBackgroundPersonFeatureCreateQueue._queue.get()

    def put(self, item: PresentationBackgroundPersonFeatureCreateQueueItem) -> None:
        if PresentationBackgroundPersonFeatureCreateQueue._queue is None:
            raise PresentationBackgroundPersonFeatureCreateQueueError("Queue not initialized")
        PresentationBackgroundPersonFeatureCreateQueue._queue.put(item)

class PresentationBackgroundPersonFeatureCreate:
    def __init__(
        self,
        logger: PresentationLogger,
        queue: PresentationBackgroundPersonFeatureCreateQueue,
        person_image: ApplicationPersonImage,
        person_feature: ApplicationPersonFeatureCreator,
    ):
        self.logger = logger
        self.queue = queue
        self.person_image = person_image
        self.person_feature = person_feature

    def setup(self, app: fastapi.FastAPI):
        app.add_event_handler("startup", self.process)

    def process(self):
        while True:
            try:
                item = self.queue.get()
                person_image = self.person_image.search_one(
                    filters=ApplicationPersonImageSearchFilters(
                        ids=[item.person_image_id],
                    )
                )
                person_feature = self.person_feature.create(person_image)
                if item.callback is not None:
                    item.callback(person_feature.id)
            except Exception as e:
                self.logger.error(f"Error background person feature create: {e}")
                continue
