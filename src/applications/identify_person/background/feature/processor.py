from repositories.database.person_features import RepositoryDatabasePersonFeatures
from modules.reid.model import ModuleReIDModel
from modules.yolo.segmentation import ModuleYoloSegmentation
from modules.yolo.segmentation.verification import ModuleYoloSegmentationVerification
from modules.yolo.pose import ModuleYoloPose
from modules.yolo.pose.verification import ModuleYoloPoseVerification
from repositories.database.person_image_paths import RepositoryDatabasePersonImagePaths
from repositories.database.person_image_paths import RepositoryDatabasePersonImagePathsFilters
from repositories.database.person_features import RepositoryDatabasePersonFeaturesFilters
from entities.person_feature import EntityPersonFeature
import uuid
from modules.storage.person_image import ModuleStoragePersonImage
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from entities.environment.storage import EntityEnvironmentStorage
from repositories.database import RepositoryDatabaseEngine
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ApplicationIdentifyPersonBackgroundFeatureProcessor:
    def __init__(
        self,
        database_person_image_paths: RepositoryDatabasePersonImagePaths,
        reid_model: ModuleReIDModel,
        yolo_segmentation: ModuleYoloSegmentation,
        yolo_segmentation_verification: ModuleYoloSegmentationVerification,
        yolo_pose: ModuleYoloPose,
        yolo_pose_verification: ModuleYoloPoseVerification,
        database_person_features: RepositoryDatabasePersonFeatures,
        storage_person_image: ModuleStoragePersonImage
    ):
        self.database_person_image_paths = database_person_image_paths
        self.reid_model = reid_model
        self.yolo_segmentation = yolo_segmentation
        self.yolo_segmentation_verification = yolo_segmentation_verification
        self.yolo_pose = yolo_pose
        self.yolo_pose_verification = yolo_pose_verification
        self.database_person_features = database_person_features
        self.storage_person_image = storage_person_image

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
        environment_storage: EntityEnvironmentStorage,
    ):
        return cls(
            database_person_image_paths=RepositoryDatabasePersonImagePaths(
                database=RepositoryDatabaseEngine(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                    database=environment_postgresql.database,
                )
            ),
            reid_model=ModuleReIDModel(),
            yolo_segmentation=ModuleYoloSegmentation(),
            yolo_segmentation_verification=ModuleYoloSegmentationVerification(),
            yolo_pose=ModuleYoloPose(),
            yolo_pose_verification=ModuleYoloPoseVerification(),
            database_person_features=RepositoryDatabasePersonFeatures(
                database=RepositoryDatabaseEngine(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                    database=environment_postgresql.database,
                )
            ),
            storage_person_image=ModuleStoragePersonImage(environment_storage.path),
        )

    async def process(self, id: uuid.UUID) -> EntityPersonFeature:
        person_image_path = self.database_person_image_paths.find_first(
            filters=RepositoryDatabasePersonImagePathsFilters(image_ids=[id])
        )
        person_image = self.storage_person_image.search(person_image_path)
        masks = self.yolo_segmentation.extract(person_image.image)
        if not self.yolo_segmentation_verification.verify(masks):
            raise ValueError("Segmentation verification failed")
        keypoints = self.yolo_pose.extract(person_image.image)
        if keypoints is None:
            raise ValueError("Pose extraction failed")
        if not self.yolo_pose_verification.verify(keypoints):
            raise ValueError("Pose verification failed")
        feature = self.reid_model.extract_feature(person_image.image, person_image.camera_id, person_image.view_id)
        logger.info(f"Feature extracted for image {id}")
        person_feature = EntityPersonFeature(
            image_id=person_image.id,
            feature=feature,
            camera_id=person_image.camera_id,
            view_id=person_image.view_id,
            timestamp=person_image.timestamp,
        )
        logger.info(f"Feature created for image {id}")
        self.database_person_features.delete(
            filters=RepositoryDatabasePersonFeaturesFilters(image_ids=[person_image.id])
        )
        logger.info(f"Feature deleted for image {id}")
        try:
            self.database_person_features.add(person_feature)
            logger.info(f"Feature added for image {id}")
        except Exception as e:
            logger.error(f"Error adding feature for image {id}: {e}")
            raise e
        return person_feature
