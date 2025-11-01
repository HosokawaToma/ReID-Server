from PIL import Image
from entities.camera_client import EntityCameraClient
from entities.image import EntityImage
from datetime import datetime
from applications.identify_person.background import ApplicationIdentifyPersonBackgroundProcess
from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from modules.datetime import ModuleDatetime
from modules.image import ModuleImage
from modules.database.mysql.camera_clients import ModuleDatabaseMySQLCameraClients
from modules.reid.model import ModuleReIDModel
from modules.storage.image import ModuleStorageImage
from modules.database.chroma.person_feature import ModuleDatabaseChromaPersonFeature
from database.chroma import DatabaseChroma
from database.mysql import DatabaseMySQL
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.mysql import EntityEnvironmentMysql
from entities.environment.chroma import EntityEnvironmentChroma
from entities.environment.storage import EntityEnvironmentStorage
from modules.yolo.segmentation import ModuleYoloSegmentation
from modules.yolo.segmentation.verification import ModuleYoloSegmentationVerification
from modules.yolo.pose import ModuleYoloPose
from modules.yolo.pose.verification import ModuleYoloPoseVerification

class ApplicationIdentifyPerson:
    def __init__(
        self,
        authenticator_camera_client: ModuleAuthenticatorCameraClient,
        database_camera_clients: ModuleDatabaseMySQLCameraClients,
        datetime_module: ModuleDatetime,
        image_module: ModuleImage,
        background_process: ApplicationIdentifyPersonBackgroundProcess
        ):
        self.authenticator_camera_client = authenticator_camera_client
        self.database_camera_clients = database_camera_clients
        self.datetime_module = datetime_module
        self.image_module = image_module
        self.background_process = background_process

    @classmethod
    def create(
        cls,
        environment_jwt: EntityEnvironmentJwt,
        environment_mysql: EntityEnvironmentMysql,
        environment_chroma: EntityEnvironmentChroma,
        environment_storage: EntityEnvironmentStorage,
        ) -> "ApplicationIdentifyPerson":
        return cls(
            authenticator_camera_client=ModuleAuthenticatorCameraClient(
                jwt_secret_key=environment_jwt.secret_key,
                jwt_algorithm=environment_jwt.algorithm,
            ),
            database_camera_clients=ModuleDatabaseMySQLCameraClients(DatabaseMySQL(
                host=environment_mysql.host,
                port=environment_mysql.port,
                user=environment_mysql.user,
                password=environment_mysql.password,
                database=environment_mysql.database,
            )),
            datetime_module=ModuleDatetime(),
            image_module=ModuleImage(),
            background_process=ApplicationIdentifyPersonBackgroundProcess(
                reid_model=ModuleReIDModel(),
                yolo_segmentation=ModuleYoloSegmentation(),
                yolo_segmentation_verification=ModuleYoloSegmentationVerification(),
                yolo_pose=ModuleYoloPose(),
                yolo_pose_verification=ModuleYoloPoseVerification(),
                storage_image=ModuleStorageImage(storage_path=environment_storage.path),
                database_person_feature=ModuleDatabaseChromaPersonFeature(DatabaseChroma(
                    host=environment_chroma.host,
                    port=environment_chroma.port,
                    secret_token=environment_chroma.secret_token,
                )),
            ),
        )

    def authenticate(self, authorization: str) -> EntityCameraClient:
        return self.authenticator_camera_client.authenticate(authorization)

    def from_iso_format(self, iso_timestamp: str) -> datetime:
        return self.datetime_module.from_iso_format(iso_timestamp)

    def decode_image(self, image: bytes) -> Image.Image:
        return self.image_module.decode(image)

    def identify(self, image: EntityImage) -> None:
        self.background_process.add(image)
