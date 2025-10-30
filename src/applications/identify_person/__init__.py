from PIL import Image
from entities.client import EntityClient
from entities.image import EntityImage
from datetime import datetime
from applications.identify_person.background import ApplicationIdentifyPersonBackgroundProcess
from modules.authenticator import ModuleAuthenticator
from modules.datetime import ModuleDatetime
from modules.image import ModuleImage
from modules.database.mysql.clients_camera import ModuleDatabaseMySQLClientsCamera
from modules.reid.model import ModuleReIDModel
from modules.storage.image import ModuleStorageImage
from modules.database.chroma.person_feature import ModuleDatabaseChromaPersonFeature
from database.chroma import DatabaseChroma
from database.mysql import DatabaseMySQL

class ApplicationIdentifyPerson:
    def __init__(
        self,
        authenticator: ModuleAuthenticator,
        database_clients_camera: ModuleDatabaseMySQLClientsCamera,
        datetime_module: ModuleDatetime,
        image_module: ModuleImage,
        background_process: ApplicationIdentifyPersonBackgroundProcess
        ):
        self.authenticator = authenticator
        self.database_clients_camera = database_clients_camera
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
            authenticator=ModuleAuthenticator(jwt_secret_key=jwt_secret_key, jwt_algorithm=jwt_algorithm),
            database_clients_camera=ModuleDatabaseMySQLClientsCamera(DatabaseMySQL(engine_url=mysql_engine_url)),
            datetime_module=ModuleDatetime(),
            image_module=ModuleImage(),
            background_process=ApplicationIdentifyPersonBackgroundProcess(
                reid_model=ModuleReIDModel(),
                storage_image=ModuleStorageImage(storage_path=storage_path),
                database_person_feature=ModuleDatabaseChromaPersonFeature(DatabaseChroma(host=chroma_host, port=chroma_port)
                )
            )
        )

    def authenticate(self, authorization: str) -> EntityClient:
        return self.authenticator.authenticate(authorization)

    def get_camera_and_view_id(self, client_id: int) -> tuple[int, int]:
        client_camera = self.database_clients_camera.get_client_camera_by_id(client_id)
        return client_camera.camera_id, client_camera.viewer_id

    def from_iso_format(self, iso_timestamp: str) -> datetime:
        return self.datetime_module.from_iso_format(iso_timestamp)

    def decode_image(self, image: bytes) -> Image.Image:
        return self.image_module.decode(image)

    def identify(self, image: EntityImage) -> None:
        self.background_process.add(image)
