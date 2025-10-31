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
        jwt_secret_key: str,
        jwt_algorithm: str,
        mysql_engine_url: str,
        storage_path: str,
        chroma_host: str,
        chroma_port: str
        ) -> "ApplicationIdentifyPerson":
        return cls(
            authenticator_camera_client=ModuleAuthenticatorCameraClient(jwt_secret_key=jwt_secret_key, jwt_algorithm=jwt_algorithm),
            database_camera_clients=ModuleDatabaseMySQLCameraClients(DatabaseMySQL(engine_url=mysql_engine_url)),
            datetime_module=ModuleDatetime(),
            image_module=ModuleImage(),
            background_process=ApplicationIdentifyPersonBackgroundProcess(
                reid_model=ModuleReIDModel(),
                storage_image=ModuleStorageImage(storage_path=storage_path),
                database_person_feature=ModuleDatabaseChromaPersonFeature(DatabaseChroma(host=chroma_host, port=chroma_port)
                )
            )
        )

    def authenticate(self, authorization: str) -> EntityCameraClient:
        return self.authenticator_camera_client.authenticate(authorization)

    def from_iso_format(self, iso_timestamp: str) -> datetime:
        return self.datetime_module.from_iso_format(iso_timestamp)

    def decode_image(self, image: bytes) -> Image.Image:
        return self.image_module.decode(image)

    def identify(self, image: EntityImage) -> None:
        self.background_process.add(image)
