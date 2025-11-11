from PIL import Image
from entities.jwt.camera_client import EntityJWTCameraClient
from entities.image import EntityImage
from datetime import datetime
from applications.identify_person.background import ApplicationIdentifyPersonBackgroundProcess
from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from modules.datetime import ModuleDatetime
from modules.image import ModuleImage
from modules.database.camera_clients import ModuleDatabaseCameraClients
from modules.reid.model import ModuleReIDModel
from modules.reid.identifier import ModuleReIDIdentifier
from modules.storage.image import ModuleStorageImage
from modules.database.person_features import ModuleDatabasePersonFeatures
from database import Database
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from entities.environment.storage import EntityEnvironmentStorage
from modules.yolo.segmentation import ModuleYoloSegmentation
from modules.yolo.segmentation.verification import ModuleYoloSegmentationVerification
from modules.yolo.pose import ModuleYoloPose
from modules.yolo.pose.verification import ModuleYoloPoseVerification
from modules.logger import ModuleLogger

class ApplicationIdentifyPerson:
    def __init__(
        self,
        database_camera_clients: ModuleDatabaseCameraClients,
        datetime_module: ModuleDatetime,
        image_module: ModuleImage,
        background_process: ApplicationIdentifyPersonBackgroundProcess
        ):
        self.database_camera_clients = database_camera_clients
        self.datetime_module = datetime_module
        self.image_module = image_module
        self.background_process = background_process

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
        environment_storage: EntityEnvironmentStorage,
        ) -> "ApplicationIdentifyPerson":
        return cls(
            database_camera_clients=ModuleDatabaseCameraClients(Database(
                host=environment_postgresql.host,
                port=environment_postgresql.port,
                user=environment_postgresql.user,
                password=environment_postgresql.password,
                database=environment_postgresql.database,
            )),
            datetime_module=ModuleDatetime(),
            image_module=ModuleImage(),
            background_process=ApplicationIdentifyPersonBackgroundProcess(
                reid_model=ModuleReIDModel(),
                reid_identifier=ModuleReIDIdentifier(threshold=0.9),
                yolo_segmentation=ModuleYoloSegmentation(),
                yolo_segmentation_verification=ModuleYoloSegmentationVerification(),
                yolo_pose=ModuleYoloPose(),
                yolo_pose_verification=ModuleYoloPoseVerification(),
                storage_image=ModuleStorageImage(storage_path=environment_storage.path),
                database_person_features=ModuleDatabasePersonFeatures(Database(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                    database=environment_postgresql.database,
                )),
                logger=ModuleLogger(environment_storage=environment_storage)
                )
            )

    async def start(self):
        await self.background_process.start()

    async def stop(self):
        await self.background_process.stop()

    def from_iso_format(self, iso_timestamp: str) -> datetime:
        return self.datetime_module.from_iso_format(iso_timestamp)

    def decode_image(self, image: bytes) -> Image.Image:
        return self.image_module.decode(image)

    async def identify(self, image: EntityImage) -> None:
        await self.background_process.add(image)
