from queue import Queue
import uuid
from dataclasses import dataclass
from typing import Callable
import fastapi

from applications.person.feature.searcher import ApplicationPersonFeatureSearcher
from applications.person.feature.searcher import ApplicationPersonFeatureSearchFilters
from applications.person.feature.identifier import ApplicationPersonFeatureIdentifier
from presentation import PresentationLogger

class PresentationBackgroundPersonFeatureIdentifyQueueError(Exception):
    pass

@dataclass
class PresentationBackgroundPersonFeatureIdentifyQueueItem:
    person_image_id: uuid.UUID
    callback: Callable[[uuid.UUID], None] | None = None

class PresentationBackgroundPersonFeatureIdentifyQueue:
    _queue: Queue[PresentationBackgroundPersonFeatureIdentifyQueueItem] | None = None

    def __init__(self):
        if PresentationBackgroundPersonFeatureIdentifyQueue._queue is None:
            PresentationBackgroundPersonFeatureIdentifyQueue._queue = Queue[PresentationBackgroundPersonFeatureIdentifyQueueItem]()

    def get(self) -> PresentationBackgroundPersonFeatureIdentifyQueueItem:
        if PresentationBackgroundPersonFeatureIdentifyQueue._queue is None:
            raise PresentationBackgroundPersonFeatureIdentifyQueueError("Queue not initialized")
        return PresentationBackgroundPersonFeatureIdentifyQueue._queue.get()

    def put(self, item: PresentationBackgroundPersonFeatureIdentifyQueueItem) -> None:
        if PresentationBackgroundPersonFeatureIdentifyQueue._queue is None:
            raise PresentationBackgroundPersonFeatureIdentifyQueueError("Queue not initialized")
        PresentationBackgroundPersonFeatureIdentifyQueue._queue.put(item)

class PresentationBackgroundPersonFeatureIdentify:
    def __init__(
        self,
        logger: PresentationLogger,
        queue: PresentationBackgroundPersonFeatureIdentifyQueue,
        searcher: ApplicationPersonFeatureSearcher,
        identifier: ApplicationPersonFeatureIdentifier,
    ):
        self.logger = logger
        self.queue = queue
        self.searcher = searcher
        self.identifier = identifier

    def setup(self, app: fastapi.FastAPI):
        app.add_event_handler("startup", self.process)

    def process(self):
        while True:
            try:
                item = self.queue.get()
                person_feature = self.searcher.search_one(
                    filters=ApplicationPersonFeatureSearchFilters(
                        ids=[item.person_image_id],
                    )
                )
                self.identifier.identify(person_feature)
                if item.callback is not None:
                    item.callback(person_feature.id)
            except Exception as e:
                self.logger.error(f"Error background person feature identify: {e}")
                continue
