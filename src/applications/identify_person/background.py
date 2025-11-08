import asyncio
from asyncio import Queue
from typing import Optional
from entities.image import EntityImage
from modules.reid.model import ModuleReIDModel
from modules.storage.image import ModuleStorageImage
from modules.database.person_features import ModuleDatabasePersonFeatures
from entities.person_feature import EntityPersonFeature
from modules.yolo.segmentation import ModuleYoloSegmentation
from modules.yolo.segmentation.verification import ModuleYoloSegmentationVerification
from modules.yolo.pose import ModuleYoloPose
from modules.yolo.pose.verification import ModuleYoloPoseVerification
from modules.logger import ModuleLogger

class ApplicationIdentifyPersonBackgroundProcess:
    def __init__(
        self,
        reid_model: ModuleReIDModel,
        yolo_segmentation: ModuleYoloSegmentation,
        yolo_segmentation_verification: ModuleYoloSegmentationVerification,
        yolo_pose: ModuleYoloPose,
        yolo_pose_verification: ModuleYoloPoseVerification,
        storage_image: ModuleStorageImage,
        database_person_features: ModuleDatabasePersonFeatures,
        logger: ModuleLogger,
    ):
        self.reid_model = reid_model
        self.yolo_segmentation = yolo_segmentation
        self.yolo_segmentation_verification = yolo_segmentation_verification
        self.yolo_pose = yolo_pose
        self.yolo_pose_verification = yolo_pose_verification
        self.storage_image = storage_image
        self.database_person_features = database_person_features
        self.queue = Queue[EntityImage]()
        self.task: Optional[asyncio.Task[None]] = None
        self.logger = logger

    async def start(self):
        self.task = asyncio.create_task(self.process_queue())
        self.logger.info("Background process started")

    async def stop(self):
        if self.task is not None:
            self.task.cancel()
        self.logger.info("Background process stopped")

    async def add(self, image: EntityImage):
        await self.queue.put(image)
        self.logger.info(f"Image added to queue: {image.id}")

    async def process_queue(self):
        while True:
            try:
                image = await self.queue.get()
            except Exception as e:
                self.logger.error(f"Error getting image from queue: {e}")
                continue
            try:
                await self.process(image)
            except Exception as e:
                self.logger.error(f"Error processing image: {image.id}: {e}")
                continue
            except asyncio.CancelledError:
                break

    async def process(self, image: EntityImage) -> None:
        self.storage_image.save(image)
        masks = self.yolo_segmentation.extract(image.image)
        if not self.yolo_segmentation_verification.verify(masks):
            return
        keypoints = self.yolo_pose.extract(image.image)
        if keypoints is None:
            return
        if not self.yolo_pose_verification.verify(keypoints):
            return
        query_feature = self.reid_model.extract_feature(image.image, image.camera_id, image.view_id)
        self.database_person_features.insert(
            EntityPersonFeature(
                id=None,
                feature=query_feature,
                camera_id=image.camera_id,
                view_id=image.view_id,
                timestamp=image.timestamp,
            )
        )
