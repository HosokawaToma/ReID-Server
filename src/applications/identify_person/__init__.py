from repositories.database.camera_clients import RepositoryDatabaseCameraClients
from repositories.database.camera_clients import RepositoryDatabaseCameraClientsFilters
from modules.datetime import ModuleDatetime
from modules.image import ModuleImage
from repositories.database import RepositoryDatabaseEngine
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from entities.environment.storage import EntityEnvironmentStorage
from modules.storage.person_image import ModuleStoragePersonImage
from entities.person_image import EntityPersonImage
from repositories.database.person_image_paths import RepositoryDatabasePersonImagePaths
from entities.person_image_path import EntityPersonImagePath

class ApplicationIdentifyPerson:
    def __init__(
        self,
        database_camera_clients: RepositoryDatabaseCameraClients,
        image_module: ModuleImage,
        datetime_module: ModuleDatetime,
        storage_person_image: ModuleStoragePersonImage,
        database_person_image_paths: RepositoryDatabasePersonImagePaths,
        ):
        self.database_camera_clients = database_camera_clients
        self.image_module = image_module
        self.datetime_module = datetime_module
        self.storage_person_image = storage_person_image
        self.database_person_image_paths = database_person_image_paths

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
        environment_storage: EntityEnvironmentStorage,
        ) -> "ApplicationIdentifyPerson":
        return cls(
            database_camera_clients=RepositoryDatabaseCameraClients(RepositoryDatabaseEngine(
                host=environment_postgresql.host,
                port=environment_postgresql.port,
                user=environment_postgresql.user,
                password=environment_postgresql.password,
                database=environment_postgresql.database,
            )),
            image_module=ModuleImage(),
            datetime_module=ModuleDatetime(),
            storage_person_image=ModuleStoragePersonImage(environment_storage.path),
            database_person_image_paths=RepositoryDatabasePersonImagePaths(RepositoryDatabaseEngine(
                host=environment_postgresql.host,
                port=environment_postgresql.port,
                user=environment_postgresql.user,
                password=environment_postgresql.password,
                database=environment_postgresql.database,
            )),
        )

    async def start(self):
        pass

    async def stop(self):
        pass

    async def proses(self, camera_client_id: str, binary_images: list[bytes]) -> list[EntityPersonImage]:
        camera_client = self.database_camera_clients.find_first(
            RepositoryDatabaseCameraClientsFilters(id=camera_client_id)
        )
        person_images = []
        for binary_image in binary_images:
            image = self.image_module.decode(binary_image)
            entity_person_image = EntityPersonImage(
                image=image,
                camera_id=camera_client.camera_id,
                view_id=camera_client.view_id,
            )
            self.storage_person_image.save(entity_person_image)
            self.database_person_image_paths.insert(EntityPersonImagePath(
                image_id=entity_person_image.id,
                camera_id=camera_client.camera_id,
                view_id=camera_client.view_id,
                timestamp=entity_person_image.timestamp,
            ))
            person_images.append(entity_person_image)
        return person_images
