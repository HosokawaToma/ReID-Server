from modules.database.person_features import ModuleDatabasePersonFeatures
from modules.reid.model import ModuleReIDModel
from modules.yolo.segmentation import ModuleYoloSegmentation
from modules.yolo.segmentation.verification import ModuleYoloSegmentationVerification
from modules.yolo.pose import ModuleYoloPose
from modules.yolo.pose.verification import ModuleYoloPoseVerification
from modules.database.person_image_paths import ModuleDatabasePersonImagePaths
from entities.person_feature import EntityPersonFeature
import uuid
from modules.storage.person_image import ModuleStoragePersonImage
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from entities.environment.storage import EntityEnvironmentStorage
from database import Database
from errors.modules.database import ErrorModuleDatabase
class ApplicationIdentifyPersonBackgroundFeatureProcessor:
    def __init__(
        self,
        database_person_image_paths: ModuleDatabasePersonImagePaths,
        reid_model: ModuleReIDModel,
        yolo_segmentation: ModuleYoloSegmentation,
        yolo_segmentation_verification: ModuleYoloSegmentationVerification,
        yolo_pose: ModuleYoloPose,
        yolo_pose_verification: ModuleYoloPoseVerification,
        database_person_features: ModuleDatabasePersonFeatures,
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
            database_person_image_paths=ModuleDatabasePersonImagePaths(
                database=Database(
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
            database_person_features=ModuleDatabasePersonFeatures(
                database=Database(
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
        person_image_path = self.database_person_image_paths.select_by_id(id)
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
        person_feature = EntityPersonFeature(
            image_id=person_image.id,
            feature=feature,
            camera_id=person_image.camera_id,
            view_id=person_image.view_id,
            timestamp=person_image.timestamp,
        )
        self.database_person_features.delete_by_image_id(person_image.id)
        self.database_person_features.insert(person_feature)
        return person_feature
